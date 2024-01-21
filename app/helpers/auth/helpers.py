import datetime
import uuid

import jwt

from database.models import UserModel
from settings import AppConfig


async def generate_jwt(
    data: dict, expiration_seconds: int = 3600
) -> str:
    exp = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=expiration_seconds)
    data["exp"] = exp

    return jwt.encode(data, AppConfig.secret_key)


async def generate_access_token(
    user: UserModel, expiration_seconds: int = 3600
) -> str:
    user_data = dict(
        id=user.id,
        role=user.role
    )
    token = await generate_jwt(user_data, expiration_seconds)
    return token


async def generate_refresh_token(
    user: UserModel, expiration_seconds: int = 3600
) -> str:
    user_data = dict(
        id=user.id,
        refresh_uuid=str(uuid.uuid4())
    )
    token = await generate_jwt(user_data, expiration_seconds)
    return token
