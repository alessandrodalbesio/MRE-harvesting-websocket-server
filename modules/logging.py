import logging
from modules.settings import *

class logger:
    def __init__(self):
        # Create the logger
        self.logger = logging.getLogger('websocket_server')
        self.logger.setLevel(logging.DEBUG)

        # Create the logging file handler
        fh = logging.FileHandler(LOGGER_FILE_NAME)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Create the logging console handler
        if LOG_ON_STDOUT:
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.DEBUG)
            c_format = logging.Formatter('[%(levelname)s] - %(message)s')
            c_handler.setFormatter(c_format)
            self.logger.addHandler(c_handler)
    
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)