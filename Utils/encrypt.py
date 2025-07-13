import os.path
import io
from cryptography.fernet import *
import json


def encriptstr(input, key=b'', encode=True):
    if key:
        fernet = Fernet(key)
        if encode:
            enc = fernet.encrypt(input.encode())
        else:
            enc = fernet.encrypt(input)
        del fernet, input
        return [enc, key]
    else:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        if encode:
            enc = fernet.encrypt(input.encode())
        else:
            enc = fernet.encrypt(input)
        return [enc, key]


def decriptstr(input, key, decode=True):
    if not key or type(key) is not bytes:
        raise ValueError('Key is empty or None. On decript something, you need the encript key.')
    fernet = Fernet(key)
    if decode:
        dec = fernet.decrypt(input).decode()
    else:
        dec = fernet.decrypt(input)
    return [dec, key]


def generatekey():
    """
    Gera uma chave Fernet.
    :return: Chave em bytes.
    """
    return Fernet.generate_key()


def encrypt_file(file, key, output, encode=True):
    if not key or type(key) is not bytes:
        raise ValueError('Key is empty or None. On decript something, you need the encript key.')

    encrypted_content = encriptstr(file.read(), key, encode)[0]
    with open(output, 'wb') as out:
        out.write(encrypted_content)


def decrypt_file(file, key: bytes, output, encode=True):
    if not key or type(key) is not bytes:
        raise ValueError('Key is empty or None. On decript something, you need the encript key.')

    decrypted_content = decriptstr(file.read(), key, not encode)[0]
    if encode:
        with open(output, 'wb') as out:
            out.write(decrypted_content)
    else:
        with open(output, 'w') as out:
            out.write(decrypted_content)
