from fastapi import FastAPI
from corn.routes.ping import router as ping_router
from corn.routes.user import router as user_router
from corn.logger import CustomLogger


def create_app():
    app = FastAPI()
    app.include_router(ping_router)
    app.include_router(user_router, prefix="/user")
    CustomLogger.set_as_default()

    return app


app = create_app()
