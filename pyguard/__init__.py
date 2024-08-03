from pyguard.config import (APP_REQUIRED_LIBRARIES, 
                            OS_SUPPORTED, 
                            PYTHON_MIN_VERSION, 
                            PYTHON_MAX_VERSION, 
                            ERROR_CHECK_PYTHON, 
                            ERROR_CHECK_OS, 
                            ERROR_CHECK_LIBRARIES,
                            BACKUP_PATH, DATA_FILE, BACKUP_INTERVAL, MAX_BACKUPS)
from pyguard.log import logger
from ui.ui import close_gui
import platform
import sys
import importlib
import shutil
from datetime import datetime
import time
import threading
import os
import json
import glob

# OS
def get_os():
    """
    Get the user's operating system name.
    Returns:
        str: The name of the operating system (e.g., 'Windows', 'MacOS', 'Linux').
    """
    try:
        os_name = platform.system()
        if os_name == "Darwin":
            return "MacOS"
        logger.info(f"OS detected: {os_name}.")
        return os_name
    except Exception as e:
        logger.warning(f"Failed to determine OS: {e}")
        return "Unknown"
    
def check_os():
    """
    Check if the user's OS is supported by Pyvel.
    Returns:
        bool: True if the user's OS is supported, False otherwise.
    """
    user_os = get_os()
    return user_os in OS_SUPPORTED

# Python        

def get_python_version():
    """
    Get the user's Python version as a tuple (major, minor).
    Returns:
        tuple: A tuple containing major and minor version numbers of Python.
    """
    return sys.version_info[:2]


def check_python_version():
    """
    Check if the user's Python version is within the required range.

    Returns:
        bool: True if the user's Python version is equal to or greater than the minimum required version
              and less than or equal to the maximum allowed version, False otherwise.
    """
    user_version = get_python_version()
    return PYTHON_MIN_VERSION <= user_version <= PYTHON_MAX_VERSION

# Libraries

def check_libraries():
    """
    Check if the required libraries are installed.
    Returns:
        bool: True if all required libraries are installed, False otherwise.
    """
    missing_libraries = []
    for lib in APP_REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib)
        except ImportError:
            missing_libraries.append(lib)
    
    if missing_libraries:
        logger.error(f"Missing libraries: {', '.join(missing_libraries)}")
        return False
    
    logger.info("Libraries Check successful: All required libraries are installed.")
    return True

# Useful

def check_all():
    """
    Run all checks for Python version and OS compatibility.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    checks = [
        ("PYTHON", check_python_version(), ERROR_CHECK_PYTHON),
        ("OS", check_os(), ERROR_CHECK_OS),
        ("LIBRARIES", check_libraries(), ERROR_CHECK_LIBRARIES)
    ]
    
    all_checks_ok = True
    
    for check_name, result, error_message in checks:
        if not result:
            logger.error(f"Check failed: {check_name} - {error_message}")
            all_checks_ok = False
        else:
            logger.info(f"Check successful: {check_name}")
    
    return all_checks_ok

def create_backup():
    """
    Create a backup of the current data file.
    
    Returns: 
        str: The path to the backup file.
    """
    backup_filename=None
    try:
        backup_filename = f"{BACKUP_PATH}backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        shutil.copy(DATA_FILE, backup_filename)
        logger.info(f"Backup created at: {backup_filename}.")
    except Exception as e:
        logger.warning(f"Couldn't create backup: {e}.")
    cleanup_old_backups()   
    return backup_filename    

def restore_latest_backup():
    """
    Restore the most recent backup file to the original data file location.
    """
    if not os.path.exists(BACKUP_PATH):
        logger.warning("No backup directory found.")
        return

    backup_files = [f for f in os.listdir(BACKUP_PATH) if f.startswith("backup_") and f.endswith(".json")]
    if not backup_files:
        logger.warning("No backup files found.")
        return

    backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(BACKUP_PATH, f)), reverse=True)
    latest_backup = backup_files[0]

    try:
        shutil.copy(os.path.join(BACKUP_PATH, latest_backup), DATA_FILE)
        logger.info(f"Restored from backup: {latest_backup}")
    except Exception as e:
        logger.error(f"Failed to restore backup: {e}")
    
def automatic_backup():
    """
    Automatically create backups at regular intervals.
    """
    while True:
        backup = create_backup()
        if backup != None:
            logger.debug("Automatic backup executed.")
        time.sleep(BACKUP_INTERVAL)

def start_backup_thread():
    """
    Start a thread for automatic backups.
    """
    backup_thread = threading.Thread(target=automatic_backup)
    backup_thread.daemon = True
    backup_thread.start()

def cleanup_old_backups():
    """
    Remove old backups to keep only the most recent ones.
    """
    backups = glob.glob(os.path.join(BACKUP_PATH, "backup_*.json"))
    backups.sort(key=os.path.getmtime, reverse=True)
    
    # Remove the oldest backups if the number exceeds the maximum allowed
    if len(backups) > MAX_BACKUPS:
        for old_backup in backups[MAX_BACKUPS:]:
            try:
                os.remove(old_backup)
                logger.info(f"Removed old backup: {old_backup}.")
            except Exception as e:
                print(f"Couldn't remove old backup: {e}.")
                logger.warning(f"Couldn't remove old backup: {e}.")
                close_gui() # shutdown app
                
    
def is_data_file_corrupted():
    """
    Check if the data file is corrupted by trying to load it.
    """
    if not os.path.exists(DATA_FILE):
        return True # File does not exist, hence it is considered corrupted
    try:
        with open(DATA_FILE, 'r') as file:
            json.load(file)
        return False # File exists and is not corrupted
    except (json.JSONDecodeError, IOError):
        return True # An error occurred while reading the file, indicating it is corrupted