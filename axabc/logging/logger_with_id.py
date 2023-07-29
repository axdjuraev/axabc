import logging
from typing import Any
from uuid import uuid4, UUID
from dataclasses import dataclass

@dataclass
class LogResult:
    id: UUID
    msg: str

class LoggerWithID(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=level)

    def debug(self, msg, *args, **kwargs):
        return self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        return self._log(logging.INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        return self._log(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        return self._log(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        return self._log(logging.CRITICAL, msg, args, **kwargs)

    def _log(self, level, msg, args, unique_id=None, **kwargs):
        if not unique_id:
            unique_id = uuid4()

        msg = f"{msg} [LOG_ID: {unique_id}]"

        if self.isEnabledFor(level):
            super()._log(level, msg, args, **kwargs)

        return LogResult(id=unique_id, msg=msg)
