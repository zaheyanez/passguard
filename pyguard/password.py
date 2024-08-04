import random
import string
from pyguard.config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

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