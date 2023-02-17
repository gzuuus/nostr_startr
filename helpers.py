from nostr import bech32
from nostr.bech32 import bech32_encode, bech32_decode, convertbits
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64, json, os, getpass
from startr_app import get_json_data
config_path=('.json')

#Nostr
def hex64_to_bech32(prefix: str, hex_key: str):
    if is_hex_key(hex_key):
        converted_bits = bech32.convertbits(bytes.fromhex(hex_key), 8, 5)
        return bech32_encode(prefix, converted_bits, bech32.Encoding.BECH32)

def bech32_to_hex64(prefix: str, b_key: str):
    hrp, data, spec = bech32_decode(b_key)
    if hrp != prefix:
        return False
    decoded = convertbits(data, 5, 8, False)
    private_key = bytes(decoded).hex()
    if not is_hex_key(private_key):
        return False
    return private_key

def is_bech32_key(hrp: str, key_str: str) -> bool:
    if key_str[:4] == hrp and len(key_str) == 63:
        return True
    return False

def is_hex_key(k):
    return len(k) == 64 and all(c in '1234567890abcdefABCDEF' for c in k)

#Encrypt/D
scrypt_n=16384
scrypt_r=8
scrypt_p=1

def encrypt_key(password, to_encrypt):
    salt_for_storage = Fernet.generate_key() 
    salt = base64.urlsafe_b64decode(salt_for_storage)
    to_encrypt = to_encrypt.encode()
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=scrypt_n,
        r=scrypt_r,
        p=scrypt_p,
    )
    _key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(_key)
    encrypted_string = f.encrypt(to_encrypt)
    encrypted_string_decode=encrypted_string.decode()
    return encrypted_string_decode, salt_for_storage

def decrypt_key(password, to_decrypt, file):
    get_all_current_scrypt=(get_json_data(file))
    kdf = Scrypt(        
        salt=base64.urlsafe_b64decode(get_all_current_scrypt[0]['scrypt']['salt']),
        length=32,
        n= get_all_current_scrypt[0]['scrypt']['n'],
        r= get_all_current_scrypt[0]['scrypt']['r'],
        p= get_all_current_scrypt[0]['scrypt']['p']
    )
    _key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(_key)
    try:
        pw = f.decrypt(to_decrypt)
        return pw.decode()
    except InvalidToken:
        print('Incorrect password')
        return False

#noscl integration
#./noscl relay | sed 's/: rw//' | xargs -L1 ./noscl relay remove [remove all relays at once in linux]


#Promt style
splash="""\

░██████╗████████╗░█████╗░██████╗░████████╗██████╗░
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
╚█████╗░░░░██║░░░███████║██████╔╝░░░██║░░░██████╔╝
░╚═══██╗░░░██║░░░██╔══██║██╔══██╗░░░██║░░░██╔══██╗
██████╔╝░░░██║░░░██║░░██║██║░░██║░░░██║░░░██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝                                                                                                          
                    """
separator="-------------------*STARTR*-------------------"
