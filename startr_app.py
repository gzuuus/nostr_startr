import re, json, os, getpass
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
            print('Startr will guide you to securely store your nostr identity')
            print('You can create a new key pair by typing "new" or you can also store your current private key securely encrypted with a password of your choice')
            print(separator)
            pk = input('Enter private key or type "new" to create a new one:')
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
            print('Enter a user and password. The password will encrypt your private key, keep it safe.')
            uss = input('Username: ')
            pw = getpass.getpass()

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

            finish = input("!!!Backup your keys. Type (y) to continue.")
            if finish.lower().strip() == 'y':
                encrypted_string=encrypt_key(PW, PK)
                dict={'pubkey': public_key, 'user': uss,'pkey': encrypted_string}
                json_object = json.dumps(dict, indent=4)
                with open(config_path, "w") as outfile:
                    outfile.write(json_object)
                #print(dict)
                complete=True
            do=input('do you want start nostr_console now? (y/n): ')
            if do.lower().strip() == 'y':
                check_nostr_console()
            else:
                return False

def startr(nostr_console):                
        print(f'User: {get_key("user")}')
        print(f'Pubkey: {get_key("pubkey")}')
        pw = getpass.getpass()
        encrypted_string=get_key("pkey")
        decrypted_string=decrypt_key(pw, encrypted_string)
        command = os.popen(f"gnome-terminal --tab -- bash -c './{nostr_console} --width=200 -m 12 -l -k {decrypted_string}'")
        print('Go!')

def get_key(skey):
    with open(config_path, 'r') as openfile:
        json_object = json.load(openfile)
    saved_key=json_object[skey]
    return saved_key

def check_nostr_console():
    nostr_console = [filename for filename in os.listdir('.') if filename.startswith("nostr_console")]
    if len(nostr_console) > 0:
        startr(nostr_console[0])
        return True
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
            check_nostr_console()
        if menu == '2':
            os.remove(config_path)
            print('reset done!')

            
