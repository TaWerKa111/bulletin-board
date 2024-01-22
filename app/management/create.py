import asyncio
import sys
import click

from app.api.auth.helpers import get_password_hash
from database import Session
from database.models import UserModel
from settings import AppConfig


@click.command()
@click.option("-l", "--login", help="Login of user", default=None)
@click.option("-pw", "--password", help="Password of user", default=None)
@click.option("-r", "--role", help="Role of user", default="admin")
def create_superuser(login, password, role):
    """
    Cmd for create user for application.

    :param login: str,
        login of user,
        Default: None
    :param password: str,
        password of user, using for admin's users
        Default: None
    :param role: str,
        role of user. Include: admin, user
        Default: admin
    """

    async def async_function():
        if role not in [AppConfig.role.admin, AppConfig.role.user]:
            print(f"Not found role {role}")
            return

        async with Session() as session:
            user = await UserModel.get_user_by_login(session, login)
            if not user:
                user = UserModel(
                    password_hash=get_password_hash(password),
                    login=login,
                    role=role,
                    name="Администратор"
                )
                session.add(user)
                await session.commit()
        print(f"User created!")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_function())
    loop.close()
    sys.exit()
