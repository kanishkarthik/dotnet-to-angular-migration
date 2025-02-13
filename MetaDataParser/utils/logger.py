import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('metadata_parser')
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create file handler with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        file_handler = logging.FileHandler(f'{log_dir}/metadata_parser_{timestamp}.log')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

logger = Logger()
