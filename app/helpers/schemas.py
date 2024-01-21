from pydantic import BaseModel


class BinaryResponse(BaseModel):
    success: bool
    message: str = None
