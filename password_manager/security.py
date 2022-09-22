import os
import base64
import hashlib
import binascii
from cryptography.fernet import Fernet


def hash_value(value: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', value.encode('utf-8'), salt, 100_000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_value(stored_value: str, provided_value: str) -> bool:
    salt = stored_value[:64]
    stored_value = stored_value[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_value.encode('utf-8'), salt.encode('ascii'), 100_000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_value


def get_key(password: str) -> bytes:
    password_part = password[64:96]
    return base64.urlsafe_b64encode(password_part.encode())


def encrypt_value(value: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()


def decrypt_value(value: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(value.encode()).decode()
