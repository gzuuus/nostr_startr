import getpass, subprocess, requests, shutil, stat, time
from helpers import *
from bip39 import bip39
from nostr.key import PrivateKey

def init():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(splash)
    print(separator)
    fetch_config_data, current_file_name=fetch_config()
    menu=input('1. Start nostr_console(nostr_console bugs), 2. Generate new key, 3. Decrypt/show saved keys, 4. Reset key, 5. Switch identity, 6. Install/update nostr_console, 7. Exit: ')
    if menu == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(splash)
        print(separator)
        check_nostr_console(False, fetch_config_data, current_file_name)
    if menu == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(splash)
        print(separator)
        setupkeys(False)
    if menu == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(splash)
        print(separator)
        print(f'> User: {fetch_config_data["user"]}')
        print(f'> Public key(HEX): {fetch_config_data["pubkey"]}')
        print(f'> Public key(npub): {fetch_config_data["npub"]}')
        print(f'> Link: https://snort.social/p/{fetch_config_data["npub"]}')
        if input('> Show private key? Type (y) to continue, (n/no) to cancel: ').lower().strip() == 'y':
            pw = getpass.getpass()
            encrypted_string=fetch_config_data['pkey']
            decrypted_string=decrypt_key(pw, encrypted_string,current_file_name)
            while decrypted_string == False:
                if input('Want to try again? (y/n)').lower().strip() == 'y':
                    pw = getpass.getpass()
                    decrypted_string=decrypt_key(pw, encrypted_string,current_file_name)
                else:
                    init()
            print(f'> Private key: {decrypted_string}')
            print(f"Bech32: ", hex64_to_bech32('nsec', decrypted_string))
            input('> Press any key to continue')
            os.system('cls' if os.name == 'nt' else 'clear')
            init()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            init()
    if menu == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(splash)
        print(separator)
        if input(f'> Are you sure to reset your keys from {current_file_name}? (y/n): ').lower().strip() == 'y':
            os.remove(current_file_name)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('reset done!')
        init()
    if menu == '5':
        init()
    if menu == '6':
        setup_nostr_console()
    if menu == '7':
        quit()


def setupkeys(status):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(splash)
    print(separator)
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
                print(separator)
                print(f"That doesn\'t seem to be a valid key, use hex or nsec")
        if step == 2:
            print(separator)
            print('2) Enter a user and password. (Info)Username its only a reference for you to recognize your keys, does not have to be your nostr username.')
            uss = input('Username: ')
            pw = getpass.getpass()
            pw_check = getpass.getpass(prompt='Repeat password: ')
            if pw == pw_check:
                if len(pw) > 0:
                    print('Username and password created.')
                    PW = pw.strip()
                    print('Password will encrypt your private key, keep it safe.')
                    step = 3
            else:
                print('Passwords do not match')
                step = 2
        if step == 3:
            print(separator)
            if PK is None:
                pk = PrivateKey()
            else:
                pk = PrivateKey(bytes.fromhex(PK))
            PK = pk.hex()
            public_key = pk.public_key.hex()
            print(f"> Username: ", uss)
            print(separator)
            print(f"> Private key:")
            print(f"Mnemonic: ", "{}".format(bip39.encode_bytes(bytes.fromhex(PK))))
            print(f"HEX: ", PK)
            print(f"Bech32: ", hex64_to_bech32('nsec', PK))
            print(separator)
            print(f"> Public key: ")
            print(f"HEX: ", public_key)
            print(f"Bech32: ", hex64_to_bech32('npub', public_key))
            print(separator)
            print('Please make a backup of your keys and password, you can also backup the file generated when you confirm (startr_config.json) This file is a keystore of your keys.')
            if input("Backup your keys!!! Type (y) to continue, (n/no) to cancel: ").lower().strip() == 'y':
                print('Keep them safe!')
            else: input("You'd better have made a backup, press any key to continue")
            encrypted_string, salt_for_storage=encrypt_key(PW, PK)
            dict={'user': uss, 'pubkey': public_key,'npub': hex64_to_bech32('npub', public_key),'pkey': encrypted_string, 'scrypt':{'salt':salt_for_storage.decode(), 'n':scrypt_n, 'r':scrypt_r, 'p':scrypt_p}}
            json_object = json.dumps(dict, indent=4)
            with open(f'stc_{uss}{config_path}', "w") as outfile:
                outfile.write(json_object)           
            complete=True
            os.system('cls' if os.name == 'nt' else 'clear')
            init()

def startr(nostr_console, session_pass, session_data, current_file_name):
    #fetch_config_data = session_data
    print(f'User: {session_data["user"]}')
    print(f'Pubkey: {session_data["pubkey"]}')
    if session_pass == False:
        pw = getpass.getpass()
    else:
        pw = session_pass
    encrypted_string=session_data["pkey"]
    decrypted_string=decrypt_key(pw, encrypted_string,current_file_name)
    while decrypted_string == False:
        if input('Want to try again? (y/n)').lower().strip() == 'y':
            pw = getpass.getpass()
            decrypted_string=decrypt_key(pw, encrypted_string,current_file_name)
        else:
            init()
    if not decrypted_string == False:
        print('Go!🔥')
        print(separator)
        command = subprocess.run([f"./{nostr_console}","-m", "12", "-l","-k",decrypted_string])
        #os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print('Try again ')
        time.sleep(1)
        init()

def fetch_config():
    fetch_config = [filename for filename in os.listdir('.') if filename.endswith(".json")]
    if len(fetch_config) == 1:
        fetch_config_data, current_file_name=get_json_data(fetch_config[0])
        print(f'> Hello: {fetch_config_data["user"]}')
        return fetch_config_data, current_file_name
    else:
        print('Select user by index number: ')
        fetch_config_data, current_file_name = get_json_data(False)
        print(f'> Hello: {fetch_config_data["user"]}')
        return fetch_config_data, current_file_name

def get_json_data(user_select):
    if user_select == False:
        fetch_config = [filename for filename in os.listdir('.') if filename.endswith(".json")]
        for (i, item) in enumerate(fetch_config):
            print([i], item)
        pick_user= (input('> Chose user by index | Type "new" | Type "x" to exit : '))
        if pick_user == 'new' or pick_user == '':
            setupkeys(False)
        if pick_user == 'x':
            quit()
        
        else:
            pick_user=int(pick_user)       
            if pick_user < len(fetch_config):
                user_select=fetch_config[pick_user]
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('out of range')
                init()
    with open(user_select, 'r') as openfile:
        json_object = json.load(openfile)
    saved_data=json_object
    return saved_data, user_select

def check_nostr_console(session_pass, session_data, session_file):
    nostr_console = [filename for filename in os.listdir('.') if (filename.startswith("nostr_console") and not filename.endswith(".zip"))]
    if len(nostr_console) > 0:
        startr(nostr_console[0], session_pass, session_data, session_file)
        return True, session_pass, session_data
    else:
        print('nostr_console no detected')
        if input(f'> Do you want to install nostr_console automatically (y/n): ').lower().strip() == 'y':
            setup_nostr_console()
        init()
        return False

def setup_nostr_console():
    url='https://api.github.com/repos/vishalxl/nostr_console/releases/latest'
    response=requests.get(url).json()
    for x in range(len(response['assets'])):
        print([x], response['assets'][x]['name'])
    selected_platform=input('> Select platform by index number:')
    if selected_platform not in ['0','1','2','3']:
        print('Selection out of range')
        time.sleep(1)
        setup_nostr_console()
    else:
        print('Downloading...')
        download_url=response['assets'][int(selected_platform)]['browser_download_url']
        local_file = response['assets'][int(selected_platform)]['name']
        data = requests.get(download_url)
        with open(local_file, 'wb')as file:
            file.write(data.content)
        shutil.unpack_archive(local_file, '.')
        nostr_console = [filename for filename in os.listdir('.') if (filename.startswith("nostr_console") and not filename.endswith(".zip"))]
        print(nostr_console[0])
        st = os.stat(nostr_console[0])
        os.chmod(nostr_console[0], st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print('Nostr_console successfully installed')
        if input('> You want to start nostr_console? Type (y/n): ').lower().strip() == 'y':
            fetch_config_data, current_file_name=fetch_config()
            check_nostr_console(False, fetch_config_data, current_file_name)
        else:
            init()

if __name__=='__main__':
    if not any(fname.endswith('.json') for fname in os.listdir('.')):
        setupkeys(False)
    else: init()
