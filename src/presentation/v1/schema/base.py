from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    status: int = Field(..., description="HTTP Status Code")
    message: str = Field(..., description="Thông báo phản hồi")
    data: Optional[T] = Field(default=None, description="Dữ liệu chính")

    class Config:
        from_attributes = True