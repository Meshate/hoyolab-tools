from .utils import log

class RequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
        log.error(message)