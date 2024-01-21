import datetime

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

from settings import config_database


class TimeStampMixin(object):
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime())
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime())


class UserModel(Base, TimeStampMixin):
    __tablename__ = f"{config_database.prefix}users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(8))
    active: Mapped[bool] = mapped_column(Boolean(), server_default="t")

    @classmethod
    async def get_user_by_login(
        cls, db_session: AsyncSession, login: str
    ) -> "UserModel":
        query = (
            select(cls)
            .where(
                cls.login == login
            )
        )
        result = await db_session.execute(query)
        return result.scalars().first()


class BulletinModel(Base):
    __tablename__ = f"{config_database.prefix}bulletins"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey(f"{config_database.prefix}users.id")
    )
