from passguard.versioning import MAJOR, MINOR, PATCH, TYPE
import requests


def get_version():
    """
    Return app current version.
    """
    version=f"v{MAJOR}.{MINOR}.{PATCH}"
    if TYPE != "production":
        version += f"-{TYPE}"
    return version

def get_last_version():
    """
    Fetches the latest version of the repository from GitHub.

    Returns:
        str: The latest version tag if available, or an error message.
    """
    try:
        response = requests.get("https://api.github.com/repos/zaheyanez/passguard/tags")
        response.raise_for_status()
        
        tags = response.json()
        version = "No tags found."
        
        if tags:
            version = tags[0]['name']
        return version
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the latest version: {e}"