from passlib.context import CryptContext


def get_pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = get_pwd_context()
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    pwd_context = get_pwd_context()
    return pwd_context.hash(password)
