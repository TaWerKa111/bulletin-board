import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.helpers import verify_password, get_password_hash
from app.api.auth.schemas import LoginSchema, SignupSchema, TokensResponse
from app.helpers.auth.helpers import generate_access_token, \
    generate_refresh_token
from app.helpers.schemas import BinaryResponse
from database import get_session
from database.models import UserModel
from settings import AppConfig

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

logger = logging.getLogger(__name__)


@router.post(
    "/login/"
)
async def login_view(
    login_data: LoginSchema,
    db_session: AsyncSession = Depends(get_session)
) -> TokensResponse:

    user = await UserModel.get_user_by_login(
        db_session, login_data.login
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Invalid login or password"
        )
    logger.debug(f"User = {user.login} = {user.password_hash}")

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=400, detail="Invalid login or password"
        )

    access_token = await generate_access_token(user)
    refresh_token = await generate_refresh_token(user)

    return TokensResponse(
        success=True,
        result={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


@router.post(
    "/signup/"
)
async def signup_view(
    signup_data: SignupSchema,
    db_session: AsyncSession = Depends(get_session)
) -> TokensResponse:
    user = await UserModel.get_user_by_login(db_session, signup_data.login)
    if user:
        raise HTTPException(status_code=400, detail="Invalid login")

    user = UserModel(
        login=signup_data.login,
        role=AppConfig.role.user,
        password_hash=get_password_hash(signup_data.password1)
    )

    access_token = await generate_access_token(user)
    refresh_token = await generate_refresh_token(user)
    db_session.add(user)
    await db_session.commit()

    return TokensResponse(
        success=True,
        result={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )

