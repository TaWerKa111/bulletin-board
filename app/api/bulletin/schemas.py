from fastapi_pagination import Page
from pydantic import BaseModel


class CreateBulletinSchema(BaseModel):
    title: str
    body: str


class BulletinSchema(CreateBulletinSchema):
    id: int
    user_id: int

    class Meta:
        from_attributes = True


class BulletinResponse(BaseModel):
    result: BulletinSchema | None


class BulletinListResponse(BaseModel):
    result: Page[BulletinSchema]
