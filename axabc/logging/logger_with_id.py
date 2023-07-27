import logging
from uuid import uuid4, UUID
from dataclasses import dataclass

@dataclass
class LogResult:
    id: UUID
    msg: str

class LoggerWithID(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=level)

    def _log(self, level, msg, args, **kwargs):
        unique_id = uuid4()
        msg = f"{msg} [LOG_ID: {unique_id}]"

        super()._log(level, msg, args, **kwargs)
        
        return LogResult(id=unique_id, msg=msg)
