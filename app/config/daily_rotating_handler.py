from datetime import datetime
from logging.handlers import RotatingFileHandler
import os


class DailyRotatingFileHandler(RotatingFileHandler):

    def __init__(self, maxBytes=0):
        super().__init__(self.get_init_baseFilename(), maxBytes=maxBytes)
    
    def get_init_baseFilename(self):
        if not os.path.isdir('logs'):
            os.makedirs('logs')
        return f"./logs/{datetime.today().strftime('%Y-%m-%d-%H-%M')}.log"
    
    def get_baseFilename(self):
        log_file_name = self.get_init_baseFilename()
        # prevent file size overflow when maxBytes is too small
        is_exists = os.path.exists(log_file_name)
        suffix = 1
        while is_exists:
            suffixed_log_file_name = f"{log_file_name}.{suffix}"
            is_exists = os.path.exists(suffixed_log_file_name)
            if is_exists:
                suffix+=1
            else:
                log_file_name = suffixed_log_file_name
        
        return log_file_name

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.baseFilename = self.get_baseFilename()
        if not self.delay:
            self.stream = self._open()
