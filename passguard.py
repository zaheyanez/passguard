from passguard import check_all, start_backup_thread, restore_latest_backup, is_data_file_corrupted
from ui.ui import start_gui
from passguard.log import logger
from passguard.config import APP_NAME, APP_VERSION, AUTO_RESTORE

# Checks
checks=check_all()

if checks==True:
    logger.info(f"{APP_NAME} {APP_VERSION}")
    if AUTO_RESTORE and is_data_file_corrupted():
        restore_latest_backup()
    start_backup_thread()
    start_gui()