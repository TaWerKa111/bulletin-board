import dataclasses

from pydantic_settings import BaseSettings


class Database(BaseSettings):
    prefix: str = "board_"
    database_url: str = "postgresql+asyncpg://admin:admin@db/board-bulletin"


@dataclasses.dataclass
class RoleConfig:
    admin: str = "admin"
    user: str = "user"


config_database = Database()
