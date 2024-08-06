import secrets
import string
from passguard.config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def generate_secure_password():
    """
    Generate a secure password with a mix of uppercase, lowercase, digits, and punctuation.
    The length of the password is randomly chosen between PASSWORD_MIN_LENGTH and PASSWORD_MAX_LENGTH.

    Returns:
        str: The generated secure password.
    """
    if PASSWORD_MIN_LENGTH < 6:
        raise ValueError("PASSWORD_MIN_LENGTH should be at least 6 characters")

    if PASSWORD_MAX_LENGTH < PASSWORD_MIN_LENGTH:
        raise ValueError("PASSWORD_MAX_LENGTH should be greater than or equal to PASSWORD_MIN_LENGTH")

    length = secrets.choice(range(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH + 1))

    all_characters = string.ascii_letters + string.digits + string.punctuation
    categories = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]

    # Ensure at least one character from each category
    password = [secrets.choice(category) for category in categories]

    # Fill the rest of the password length with random characters
    password += [secrets.choice(all_characters) for _ in range(length - len(password))]

    # Shuffle the result to ensure randomness
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)
