from fastapi import APIRouter, Depends
from corn.config import get_settings, Settings


router = APIRouter()


@router.get("/ping")
async def ping(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.env,
        "database_url": settings.database_url
    }
