import random
import string
from cryptography.fernet import Fernet
import os
from pyguard.config import KEY_FILE, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def load_key():
    """
    Load the secret key from a file or generate a new one if the file does not exist.

    Returns:
        bytes: The secret key used for encryption and decryption.
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as file:
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

def generate_secure_password():
    """
    Generate a secure password with a mix of uppercase, lowercase, digits, and punctuation.
    The length of the password is randomly chosen between PASSWORD_MIN_LENGTH and PASSWORD_MAX_LENGTH.

    Returns:
        str: The generated secure password.
    """
    length = random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
    
    if length < 6:
        raise ValueError("Password length should be at least 6 characters")

    all_characters = string.ascii_letters + string.digits + string.punctuation

    # Ensure at least one character from each category
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Fill the rest of the password length with random characters
    password += random.choices(all_characters, k=length - len(password))

    # Shuffle the result to ensure randomness
    random.shuffle(password)
    
    return ''.join(password)
