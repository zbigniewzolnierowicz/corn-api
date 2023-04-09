from fastapi import FastAPI
from corn.routes.ping import router as ping_router
from corn.routes.user import router as user_router
import logging


class CustomLogger(logging.Logger):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def colorizer(self, color: str):
        return f"{color}[%(levelname)s]{self.reset} [%(asctime)s]: %(message)s"

    def __init__(self):
        logging.addLevelName(logging.CRITICAL, "FATAL")
        super().__init__("")
        self.FORMATS = {
            logging.DEBUG: self.colorizer(self.grey),
            logging.INFO: self.colorizer(self.blue),
            logging.WARNING: self.colorizer(self.yellow),
            logging.ERROR: self.colorizer(self.red),
            logging.CRITICAL: self.colorizer(self.bold_red),
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(CustomLogger())
logger.addHandler(stdout_handler)


def create_app():
    app = FastAPI()
    app.include_router(ping_router)
    app.include_router(user_router, prefix="/user")

    return app


app = create_app()
