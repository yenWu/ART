import logging

class Log(logging.Logger):

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, level, logger):
        logging.basicConfig(level=level)
        self.logger = logging.getLogger(logger)

    def debug(self, log):
        self.logger.debug(log)

    def info(self, log):
        self.logger.info(log)

    def warning(self, log):
        self.loger.warning(log)

    def error(self, log):
        self.logger.error(log)

    def critical(self, log):
        self.logger.critical(log)
