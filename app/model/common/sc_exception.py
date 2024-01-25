from .enums import ErrorCode


class SCException(Exception):
    def __init__(self, status_code: int, error_code: ErrorCode, **kwargs):
        self.status_code = status_code
        self.error_code = error_code
        self.kwargs = kwargs
