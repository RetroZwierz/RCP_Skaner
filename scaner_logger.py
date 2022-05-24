from asyncio.log import logger
import logging
from config import LOG_FILE

#Creating and Configuring Logger

class Scaner_Logger:

    def __init__(self):
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = LOG_FILE,filemode = "a",format = Log_Format, level = logging.DEBUG)
        self.logger = logging.getLogger()

    def log_Error(self, message):
        self.logger.error(message)

    def log_Info(self, message):
        self.logger.info(message)