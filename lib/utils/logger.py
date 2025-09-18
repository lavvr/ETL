import logging

class ETLLogger:
    def __init__(self,
             name='etl_logger',
             log_level='INFO',
             log_to_console=True,
             log_to_file=True,
             log_file_path=None):
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level))

        formatter = logging.Formatter()

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_to_file:
            if log_file_path is None:
                log_file_path = '../../etl.log'

            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def exception(self, message):
        self.logger.exception(message)

logger = ETLLogger()