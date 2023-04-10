import logging


class CustomLogger(logging.Logger, logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def colorizer(self, color: str) -> str:
        return f"{color}[%(levelname)s]{self.reset} [%(asctime)s]: %(message)s"

    def __init__(self) -> None:
        logging.addLevelName(logging.CRITICAL, "FATAL")
        super().__init__("")
        self.FORMATS = {
            logging.DEBUG: self.colorizer(self.grey),
            logging.INFO: self.colorizer(self.blue),
            logging.WARNING: self.colorizer(self.yellow),
            logging.ERROR: self.colorizer(self.red),
            logging.CRITICAL: self.colorizer(self.bold_red),
        }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    @classmethod
    def set_as_default(self) -> None:
        logger = logging.getLogger("uvicorn")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(CustomLogger())
        logger.addHandler(stdout_handler)
