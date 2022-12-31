import getpass
from helpers import *
from bip39 import bip39
from nostr.key import PrivateKey

def setupkeys(status):
    PK=None
    PW=None
    complete = status
    step = 1
    while not complete:
        if step == 1:
            print('Startr will guide you to securely store or create your nostr identity')
            print('Follow the steps to create a new key pair or store your current private key')
            print(separator)
            pk = input('1) Enter private key (copy/paste your current private-key or type "new" to create a new one): ')
            if pk.lower().strip() == 'new':
                step = 2
            elif is_hex_key(pk.strip()):
                step = 2
                PK = pk.strip()
            elif is_bech32_key('nsec', pk.strip()):
                step = 2
                PK = bech32_to_hex64('nsec', pk.strip())
            else:
                print(f"That doesn\'t seem to be a valid key, use hex or nsec")
        if step == 2:
            print(separator)
            print('2) Enter a user and password.')
            uss = input('Username: ')
            print(f'(Info)Username: {uss} its only a reference for you to recognize your keys, does not have to be your nostr username.')
            pw = getpass.getpass()
            print('Password will encrypt your private key, keep it safe.')

            if len(pw) > 0:
                print('Password and username created.')
                PW = pw.strip()
                step = 3
        if step == 3:
            print(separator)
            if PK is None:
                pk = PrivateKey()
            else:
                pk = PrivateKey(bytes.fromhex(PK))
            PK = pk.hex()
            public_key = pk.public_key.hex()
            print(f"Username: ", uss)
            print(separator)
            print(f"Private key:")
            print(f"Mnemonic: ", "{}".format(bip39.encode_bytes(bytes.fromhex(PK))))
            print(f"HEX: ", PK)
            print(f"Bech32: ", hex64_to_bech32('nsec', PK))
            print(separator)
            print(f"Public key: ")
            print(f"HEX: ", public_key)
            print(f"Bech32: ", hex64_to_bech32('npub', public_key))
            print(separator)
            print('Please make a backup of your keys and password, you can also backup the file generated when you confirm (startr_config.json) This file is a keystore of your keys.')
            finish = input("!!!Backup your keys. Type (y/n) to continue.")
            if finish.lower().strip() == 'y':
                encrypted_string=encrypt_key(PW, PK)
                dict={'pubkey': public_key, 'user': uss,'pkey': encrypted_string}
                json_object = json.dumps(dict, indent=4)
                with open(config_path, "w") as outfile:
                    outfile.write(json_object)
                complete=True
            do=input('do you want start nostr_console now? (y/n): ')
            if do.lower().strip() == 'y':
                check_nostr_console(PW)
            else:
                return False

def startr(nostr_console, session_pass):                
        print(f'User: {get_key("user")}')
        print(f'Pubkey: {get_key("pubkey")}')
        if session_pass == False:
            pw = getpass.getpass()
        else:
            pw = session_pass
        encrypted_string=get_key("pkey")
        decrypted_string=decrypt_key(pw, encrypted_string)
        if not decrypted_string == False:
            command = os.popen(f"gnome-terminal --tab -- bash -c './{nostr_console} --width=200 -m 12 -l -k {decrypted_string}'")
            print('Go!🔥')

def check_nostr_console(session_pass):
    nostr_console = [filename for filename in os.listdir('.') if filename.startswith("nostr_console")]
    if len(nostr_console) > 0:
        startr(nostr_console[0], session_pass)
        return True, session_pass
    else:
        print('nostr_console no detected please go to https://github.com/vishalxl/nostr_console/releases and put the release file in the same path as startr')
        return False

if __name__=='__main__':
    print(splash)
    if not os.path.exists(config_path):
        setupkeys(False)
    else:
        print(f'hello: {get_key("user")}')
        menu=input('1. start nostr_console, 2. Reset keys: ')
        if menu == '1':
            check_nostr_console(False)
        if menu == '2':
            os.remove(config_path)
            print('reset done!')

            
