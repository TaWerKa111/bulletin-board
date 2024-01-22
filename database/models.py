import datetime

from sqlalchemy import (
    String, DateTime, Integer, ForeignKey, select, Text
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

from settings import config_database

from fastapi_pagination import Params as PageParams, Page
from fastapi_pagination.ext.sqlalchemy import paginate


class TimeStampMixin(object):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), default=datetime.datetime.utcnow())
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), nullable=True)


class UserModel(Base, TimeStampMixin):
    __tablename__ = f"{config_database.prefix}users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(8))
    blocked_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), nullable=True)
    delete_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), nullable=True
    )

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

    @classmethod
    async def get_users(
        cls, db_session: AsyncSession, page_params: PageParams, login: str,
        is_blocked: True = False
    ) -> Page:
        query = select(cls)

        if login:
            login_str = f"%{login}%"
            query = query.where(cls.login.ilike(login_str))

        if is_blocked:
            query = query.where(cls.blocked_at.isnot(None))

        result = await paginate(db_session, query, page_params)
        return result

    @classmethod
    async def get_user_by_id(
        cls, db_session: AsyncSession, user_id: int
    ) -> "UserModel":
        query = (
            select(cls)
            .where(
                cls.id == user_id
            )
        )
        result = await db_session.execute(query)
        return result.scalars().first()


class BulletinModel(Base, TimeStampMixin):
    __tablename__ = f"{config_database.prefix}bulletins"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey(f"{config_database.prefix}users.id")
    )
    title: Mapped[str] = mapped_column(String(256))
    body: Mapped[str] = mapped_column(Text())
    deleted_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    @classmethod
    async def get_bulletin(
        cls, db_session: AsyncSession, bulletin_id: int, user_id: int = None
    ) -> "BulletinModel":
        query = (
            select(cls)
            .where(
                cls.id == bulletin_id,
                cls.deleted_at.is_(None)
            )
        )
        if user_id:
            query = query.where(cls.user_id == user_id)
        result = await db_session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_bulletins(
        cls, db_session: AsyncSession, page_params: PageParams,
        user_id: int = None,
    ) -> Page:
        query = (
            select(cls)
            .where(
                cls.deleted_at.is_(None)
            )
        )
        if user_id:
            query = query.where(cls.user_id == user_id)

        result = await paginate(db_session, query, page_params)
        return result


class CommentModel(Base, TimeStampMixin):
    __tablename__ = f"{config_database.prefix}comments"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey(f"{config_database.prefix}users.id")
    )
    message: Mapped[str] = mapped_column(Text())
