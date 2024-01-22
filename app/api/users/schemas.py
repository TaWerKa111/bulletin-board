from datetime import datetime

from fastapi_pagination import Page
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str | None
    created_at: datetime
    blocked_at: datetime | None
    delete_at: datetime | None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    result: Page[UserSchema]
