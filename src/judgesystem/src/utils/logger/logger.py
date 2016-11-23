#_*_coding=utf-8_*_
import logging
import logging.handlers

class Logger():
    '''
    '''

    def __init__(self, log_position):
        self.logger = logging.getLogger(log_position)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s-%(name)s-%(message)s'
        formatter = logging.Formatter(fmt)
        handler = logging.handlers.RotatingFileHandler(log_position, maxBytes = 1048576, backupCount = 5)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)


    def info(self, message):
        self.logger.info(message)


    def error(self, message):
        self.logger.error(message)


    def warning(self, message):
        self.logger.warning(message)
