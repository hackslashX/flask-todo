""" Cryptography Routines for Encryption and Key Generation """

import base64
import hashlib
import random
from io import BytesIO

from Crypto.Cipher import AES


def generate_aes_key(
    password: str,
) -> (str, str,):
    """Generate a random AES key

    Args:
        password (str): The password to use to generate the key.

    Returns:
        (str, str): The key and salt.
    """
    salt = hex(random.getrandbits(256))[2:]
    salt = hashlib.md5(salt.encode("utf-8"))
    password_hash = hashlib.md5(password.encode("utf-8"))
    key = hashlib.md5(
        salt.hexdigest().encode("utf-8") + password_hash.hexdigest().encode("utf-8")
    ).hexdigest()
    salt = salt.hexdigest()
    return key, salt


def generate_determinstic_aes_key(password: str, salt: str) -> bytes:
    """Generate a deterministic AES key

    Args:
        password (str): The password to use to generate the key.
        salt (str): The salt to use to generate the key.

    Returns:
        bytes: The key.
    """
    password_hash = hashlib.md5(password.encode("utf-8"))
    key = hashlib.md5(
        salt.encode("utf-8") + password_hash.hexdigest().encode("utf-8")
    ).hexdigest()
    return key.encode("utf-8")


def encrypt_data_aes(key: bytes, data: bytes) -> str:
    """Encrypt data using AES

    Args:
        key (bytes): The key to use to encrypt the data.
        data (bytes): The data to encrypt.

    Returns:
        str: The encrypted data.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted_data = BytesIO()
    for obj in (cipher.nonce, tag, ciphertext):
        encrypted_data.write(obj)
    encrypted_data.seek(0)
    # Convert encrypted data to Base64 string
    encrypted_data = base64.b64encode(encrypted_data.read())
    return encrypted_data.decode("utf-8")
