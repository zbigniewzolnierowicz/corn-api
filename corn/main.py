import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from corn.config import pg_settings
from corn.logger import CustomLogger
from corn.routes.ping import router as ping_router
from corn.routes.user import router as user_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(ping_router)
    app.include_router(user_router, prefix="/user")
    CustomLogger.set_as_default()

    try:
        engine = create_engine(pg_settings.base_url())
        engine.connect()
    except OperationalError as ex:
        logging.error("Could not connect to database.")
        raise ex

    return app


app = create_app()
