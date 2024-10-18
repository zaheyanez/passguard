from cryptography.fernet import Fernet
import os
from passguard.config import KEY_PATH, KEY_FILE

def load_key():
    """
    Load the secret key from a file or generate a new one if the file does not exist.

    Args:
        key_path (str): The directory path where the key file is stored.
        key_file (str): The name of the key file.

    Returns:
        bytes: The secret key used for encryption and decryption.
    """
    if not os.path.exists(KEY_PATH):
        os.makedirs(KEY_PATH)
    
    full_key_path = os.path.join(KEY_PATH, KEY_FILE)
    
    if os.path.exists(full_key_path):
        with open(full_key_path, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(full_key_path, 'wb') as file:
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


