import logging
from passguard.config import LOG_FILE, LOG_FORMAT, LOG_LEVEL

class Logger:
    def __init__(self):
        """
        Initializes the Logger class.
        
        Sets up the logging configuration with a file handler, log level, and formatter.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(LOG_LEVEL)

        # Create a file handler to log to a file
        file_handler = logging.FileHandler(LOG_FILE, mode='a')
        file_handler.setLevel(LOG_LEVEL)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger only if it doesn't already have handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        Returns the configured logger.
        
        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger

# Initialize and retrieve the logger instance
logger = Logger().get_logger()
