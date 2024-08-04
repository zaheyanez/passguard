import random
import string
from cryptography.fernet import Fernet
import os
from pyguard.config import KEY_PATH, KEY_FILE, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def load_key():
    """
    Load the secret key from a file or generate a new one if the file does not exist.

    Returns:
        bytes: The secret key used for encryption and decryption.
    """
    KEY=f"{KEY_PATH} {KEY_FILE}"
    if os.path.exists(KEY):
        with open(KEY, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY, 'wb') as file:
            file.write(key)
    return key

def encrypt_password(password):
    """
    Encrypt a password using Fernet symmetric encryption.

    Args:
        password (str): The plain text password to encrypt.

    Returns:
        str: The encrypted password, encoded in base64.
    """
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password):
    """
    Decrypt an encrypted password using Fernet symmetric encryption.

    Args:
        encrypted_password (str): The encrypted password, encoded in base64.

    Returns:
        str: The plain text password.
    """
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode()).decode()
    return decrypted_password


