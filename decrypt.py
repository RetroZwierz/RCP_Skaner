import base64
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Util.Padding import unpad
from config import SECRET_KEY, IV, SALT


def base64_decoding(input):
    return base64.decodebytes(input.encode('ascii'))


def decryption(encrypted_string):
    encrypted_string = base64_decoding(encrypted_string)
    salt = base64_decoding(SALT)
    iv = base64_decoding(IV)
    secret_key = SECRET_KEY.encode('ascii')
    decryption_key = PBKDF2(
        secret_key, salt, 32, count=10000,
        hmac_hash_module=SHA1
    )
    cipher = AES.new(decryption_key, AES.MODE_CBC, iv)
    decrypted_string = unpad(cipher.decrypt(encrypted_string), AES.block_size)

    return decrypted_string.decode('UTF-8')
