import datetime

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params as PageParams

from app.api.users.schemas import UserListResponse
from app.helpers.auth.classes import JWTBearer
from app.helpers.schemas import BinaryResponse
from database import get_session
from database.models import UserModel
from settings import AppConfig

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/"
)
async def get_users(
    login: str = None,
    db_session: AsyncSession = Depends(get_session),
    page_params: PageParams = Depends(),
    jwt_payload: dict = Depends(JWTBearer(roles=[AppConfig.role.admin]))
):
    users = await UserModel.get_users(
        db_session, page_params, login
    )

    return UserListResponse(result=users)


@router.patch("/{id}/block/")
async def block_user(
    user_id: int = Path(alias="id"),
    db_session: AsyncSession = Depends(get_session),
    jwt_payload: dict = Depends(JWTBearer(roles=[AppConfig.role.admin]))
):

    user = await UserModel.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(
            status_code=400, detail="Not found user!")

    if user.id == jwt_payload.get("user_id"):
        raise HTTPException(
            status_code=400, detail="You can't block yourself"
        )

    user.blocked_at = datetime.datetime.utcnow()
    db_session.add(user)
    await db_session.commit()

    return BinaryResponse(success=True, message="Success blocked user!")


@router.patch("/{id}/unblock/")
async def block_user(
    user_id: int = Path(alias="id"),
    db_session: AsyncSession = Depends(get_session),
    jwt_payload: dict = Depends(JWTBearer(roles=[AppConfig.role.admin]))
):
    user = await UserModel.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(
            status_code=400, detail="Not found user!")

    if user.id == jwt_payload.get("user_id"):
        raise HTTPException(
            status_code=400, detail="You can't unblock yourself"
        )

    user.blocked_at = None
    db_session.add(user)
    await db_session.commit()

    return BinaryResponse(success=True, message="Success unblocked user!")


@router.delete("/{id}/")
async def delete_user(
    user_id: int = Path(alias="id"),
    db_session: AsyncSession = Depends(get_session),
    jwt_payload: dict = Depends(JWTBearer(roles=[AppConfig.role.admin]))
):
    user = await UserModel.get_user_by_id(db_session, user_id)

    if not user:
        raise HTTPException(
            status_code=400, detail="Not found user!")

    if user.id == jwt_payload.get("user_id"):
        raise HTTPException(
            status_code=400, detail="You can't delete yourself"
        )

    user.delete_at = datetime.datetime.utcnow()
    db_session.add(user)
    await db_session.commit()

    return BinaryResponse(success=True, message="Success deleted user!")
