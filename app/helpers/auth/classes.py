from typing import List

import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from settings import AppConfig


class JWTBearer(HTTPBearer):
    def __init__(self, roles: List[str] = None):
        self.roles = roles
        super().__init__()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request)
        if credentials:
            if not (payload := self.verify_jwt(credentials.credentials)):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            if payload.get("refresh_uuid"):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            if self.roles and payload.get("role") not in self.roles:
                raise HTTPException(
                    status_code=403, detail="You dont have permissions.")
            return payload
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token, AppConfig.secret_key, algorithms=AppConfig.jwt_alg)
            return payload
        except Exception as err:
            print(f"err {err}")
            return None
