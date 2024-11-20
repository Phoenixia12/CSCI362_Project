import os
import logging
import logging.config

# Set BASE_DIR to the directory containing app_logs.log
BASE_DIR = r"C:\Users\Diego\Downloads\CSCI362_Project-main (2)\CSCI362_Project-main"
log_file_path = os.path.join(BASE_DIR, 'app_logs.log')
print("Logging to:", log_file_path)  # Confirm the log file path

# Configure logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': log_file_path,  # Pointing to the correct log file
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Set up logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('django')

# Log a test message
logger.info("This is a test log message to the original app_logs.log.")