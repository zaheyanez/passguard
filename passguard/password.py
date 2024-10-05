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
    # Minimum validations
    if PASSWORD_MIN_LENGTH < 6:
        raise ValueError("PASSWORD_MIN_LENGTH should be at least 6 characters")
    if PASSWORD_MAX_LENGTH < PASSWORD_MIN_LENGTH:
        raise ValueError("PASSWORD_MAX_LENGTH should be greater than or equal to PASSWORD_MIN_LENGTH")

    # Calculate password length
    length = secrets.randbelow(PASSWORD_MAX_LENGTH - PASSWORD_MIN_LENGTH + 1) + PASSWORD_MIN_LENGTH

    # Define character categories and build the password
    categories = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]
    password = [secrets.choice(cat) for cat in categories]

    # Fill the rest of the password
    all_characters = ''.join(categories)  # Combine all categories into a single string
    password += [secrets.choice(all_characters) for _ in range(length - len(password))]

    # Shuffle to ensure random order and convert to string
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
