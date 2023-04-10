from fastapi import FastAPI

from corn.logger import CustomLogger
from corn.routes.ping import router as ping_router
from corn.routes.user import router as user_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(ping_router)
    app.include_router(user_router, prefix="/user")
    CustomLogger.set_as_default()

    return app


app = create_app()
