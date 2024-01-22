import datetime

from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi_pagination import Params as PageParams

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.bulletin.schemas import BulletinResponse, BulletinListResponse, \
    CreateBulletinSchema
from app.helpers.auth.classes import JWTBearer
from app.helpers.schemas import BinaryResponse
from database import get_session
from database.models import BulletinModel

router = APIRouter(
    prefix="/bulletins",
    tags=["Bulletin"],
)


@router.post(
    "/"
)
async def create_bulletin_view(
    bulletin: CreateBulletinSchema,
    db_session: AsyncSession = Depends(get_session),
    jwt_payload: dict = Depends(JWTBearer())
):

    new_bulletin = BulletinModel(
        title=bulletin.title,
        body=bulletin.body,
        user_id=jwt_payload.get("user_id")
    )

    db_session.add(new_bulletin)
    await db_session.commit()

    return BinaryResponse(success=True, message="Success create bulletin!")


@router.get(
    "/"
)
async def get_bulletins_view(
    user_id: int | None = None,
    db_session: AsyncSession = Depends(get_session),
    page_params: PageParams = Depends()
):
    bulletins = await BulletinModel.get_bulletins(
        db_session, page_params, user_id=user_id
    )
    return BulletinListResponse(result=bulletins)


@router.get(
    "/{id}/"
)
async def get_detail_bulletin_view(
    bulletin_id: int = Path(alias="id"),
    db_session: AsyncSession = Depends(get_session)
):
    bulletin = await BulletinModel.get_bulletin(
        db_session, bulletin_id
    )
    return BulletinResponse(result=bulletin)


@router.delete(
    "/{id}/"
)
async def delete_bulletin_view(
    bulletin_id: int = Path(alias="id"),
    db_session: AsyncSession = Depends(get_session),
    jwt_payload: dict = Depends(JWTBearer())
):
    bulletin = await BulletinModel.get_bulletin(
        db_session, bulletin_id, user_id=jwt_payload.get("user_id")
    )
    if not bulletin:
        raise HTTPException(status_code=404, detail="Not found Bulletin!")

    bulletin.deleted_at = datetime.datetime.utcnow()
    db_session.add(bulletin)
    await db_session.commit()

    return BinaryResponse(
        succes=True, message=f"Success deleted bulletin by id = {bulletin_id}")
