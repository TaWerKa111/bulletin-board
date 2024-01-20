from fastapi import APIRouter

from settings import config_database

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login/"
)
async def login():
    return {"message": config_database.database_url}
