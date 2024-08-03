from pyguard.versioning import MAJOR, MINOR, PATCH

def get_version():
    """
    Return app current version.
    """
    return f"v{MAJOR}.{MINOR}.{PATCH}"