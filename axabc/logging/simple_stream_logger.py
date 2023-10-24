import logging
from datetime import datetime

from .logger_with_id import LoggerWithID


class SimpleStreamLogger(LoggerWithID):
    def __init__(self, name, level=logging.DEBUG):
        super().__init__(name, level=level)

        # Create a formatter to specify the log record's format
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create a console handler to display logs on the console
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
        self.addHandler(self.stream_handler)

