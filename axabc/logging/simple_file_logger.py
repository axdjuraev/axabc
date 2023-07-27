import logging
from .logger_with_id import LoggerWithID
from datetime import datetime


class SimpleFileLogger(LoggerWithID):
    def __init__(self, name, level=logging.DEBUG, filename=...):
        super().__init__(name, level=level)

        # Create a formatter to specify the log record's format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create a console handler to display logs on the console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)
        
        if filename is not None:
            if filename is ...:
                date = datetime.now().strftime('%Y-%m-%d')
                filename = f"{name}-{date}.log"

            # Create a file handler to write logs to a file
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            
            self.addHandler(file_handler)
