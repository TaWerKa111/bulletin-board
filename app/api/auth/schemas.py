from pydantic import BaseModel

from app.helpers.schemas import BinaryResponse


class LoginSchema(BaseModel):
    login: str
    password: str


class SignupSchema(BaseModel):
    login: str
    password1: str
    password2: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokensResponse(BinaryResponse):
    result: TokensSchema
