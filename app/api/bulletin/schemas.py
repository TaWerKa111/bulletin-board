from fastapi_pagination import Page
from pydantic import BaseModel


class CreateBulletinSchema(BaseModel):
    title: str
    body: str


class DetailBulletinSchema(CreateBulletinSchema):
    id: int
    user_id: int

    class Meta:
        from_attributes = True


class MinBulletinSchema(BaseModel):
    id: int
    user_id: int
    title: int

    class Meta:
        from_attributes = True


class BulletinResponse(BaseModel):
    result: MinBulletinSchema | None


class BulletinListResponse(BaseModel):
    result: Page[DetailBulletinSchema]
