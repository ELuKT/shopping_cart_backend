import logging
import inspect
from app.config.common_middleware import get_request_id

class LogService:
    system_logger = logging.getLogger('system_logger')

    def format_pattern(msg):
        return f"[{get_request_id()}] {inspect.stack()[2][1]}: line {inspect.stack()[2][2]} - {msg}"
    
    @classmethod
    def debug(cls, msg):
        cls.system_logger.debug(cls.format_pattern(msg))
        
    @classmethod
    def info(cls, msg):
        cls.system_logger.info(cls.format_pattern(msg))

    @classmethod
    def error(cls, msg, *args):
        cls.system_logger.error(cls.format_pattern(msg), *args, exc_info=True)