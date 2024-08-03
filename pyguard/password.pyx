from libc.stdlib cimport rand, srand
from libc.time cimport time
from random import choice, randint, shuffle
import string
from pyguard.config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH

def generate_secure_password():
    cdef int length = randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
    if length < 6:
        raise ValueError("Password length should be at least 6 characters")
    cdef str all_characters = string.ascii_letters + string.digits + string.punctuation
    cdef list password = [
        choice(string.ascii_uppercase),
        choice(string.ascii_lowercase),
        choice(string.digits),
        choice(string.punctuation)
    ]
    password += [choice(all_characters) for _ in range(length - len(password))]
    shuffle(password)
    return ''.join(password)