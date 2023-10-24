import logging
from datetime import datetime

from .simple_stream_logger import SimpleStreamLogger


class SimpleFileLogger(SimpleStreamLogger):
    def __init__(self, name, level=logging.DEBUG, filename=...):
        super().__init__(name, level=level)
        
        if filename is not None:
            if filename is ...:
                date = datetime.now().strftime('%Y-%m-%d')
                filename = f"{name}-{date}.log"

            # Create a file handler to write logs to a file
            self.file_handler = logging.FileHandler(filename)
            self.file_handler.setFormatter(self.formatter)
            
            self.addHandler(self.file_handler)

