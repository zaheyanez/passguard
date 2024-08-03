from pyguard.version import get_version

# APP CONFIGURATION
APP_NAME="PyGuard"
APP_VERSION=get_version()
APP_ICON="resources/icons/pyguard/icon.png"
APP_REPOSITORY="https://github.com/zaheyanez/pyguard"
APP_AUTHOR="Zaheyanez"
APP_LICENSE="MIT"
APP_REQUIRED_LIBRARIES=[
    "PyQt5",
    "cryptography",
]
APP_THEME_COLOR="#0078D4"
APP_FONT="Arial"
#--


# PASSWORD CONFIGURATION
PASSWORD_MIN_LENGTH=20
PASSWORD_MAX_LENGTH=25

# PYTHON CONFIGURATION
PYTHON_MIN_VERSION=(3,9)
PYTHON_MAX_VERSION=(3,11)

# FILES (DIRECT PATH)
LOG_FILE="app.log"
KEY_FILE="secret.key"
DATA_FILE="passwords.json"

# PATHS
BACKUP_PATH="pyguard/backups/" # Remember put '/' at the end

# LOGGING CONFIGURATION
LOG_LEVEL="DEBUG"
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# BACKUP CONFIGURATION
BACKUP_INTERVAL = 3600  # Interval in seconds for automatic backups (1 hour)
AUTO_RESTORE = True  # If True, PyGuard will automatically restore the most recent backup if 'passwords.json' is missing or corrupted at startup
MAX_BACKUPS = 10  # Maximum number of backup files to keep

# OS CONFIGURATION
OS_SUPPORTED=[
    "Windows",
    "MacOS",
    "Linux"
]

# ERROR MESSAGES
ERROR_CHECK_PYTHON=f"Your Python version must be higher than {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} and lower or equal to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}. Please update your Python installation."
ERROR_CHECK_OS = f"Your OS is not supported. Supported OS are: {', '.join(OS_SUPPORTED)}."
ERROR_CHECK_LIBRARIES = f"Required libraries are missing. Please check {LOG_FILE} for more details."
