import dataclasses
import logging
import logging.config
import os
import sys

import yaml
from pydantic_settings import BaseSettings


class Database(BaseSettings):
    prefix: str = "board_"
    database_url: str = "postgresql+asyncpg://admin:admin@db/board-bulletin"


@dataclasses.dataclass
class RoleConfig:
    admin: str = "admin"
    user: str = "user"


@dataclasses.dataclass
class AppConfig:
    secret_key = "secrets"
    role = RoleConfig()
    database = Database()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logging_conf = base_dir + "/logging.yml"


config_database = Database()


# Logger config read
if (
    os.path.isfile(AppConfig.logging_conf)
    and os.access(AppConfig.logging_conf, os.R_OK)
):
    lc_stream = open(AppConfig.logging_conf, "r")
    lc_conf = yaml.load(lc_stream, Loader=yaml.FullLoader)
    lc_stream.close()
    logging.config.dictConfig(lc_conf)
else:
    print(
        f"ERROR: logger config file '{AppConfig.logging_conf}' not exists or "
        f"not readable\n"
    )
    sys.exit(1)
