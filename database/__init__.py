from settings import Database

from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(Database.url)
Session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
