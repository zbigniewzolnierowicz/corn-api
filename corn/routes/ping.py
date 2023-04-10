from fastapi import APIRouter, Depends

from corn.config import settings
from corn.dao.user import UserDAO

router = APIRouter()


@router.get("/ping")
async def ping(user_dao: UserDAO = Depends(UserDAO)) -> dict[str, str]:
    return {
        "ping": "pong!",
        "environment": settings.env,
        "database_url": settings.database_url
    }
