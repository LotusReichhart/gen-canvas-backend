from typing import Optional, List
from pydantic import BaseModel


class BannerResponse(BaseModel):
    id: int
    title: str
    image_url: str
    action_url: Optional[str] = None
    display_order: int

    class Config:
        from_attributes = True

class BannerListResponse(BaseModel):
    banners: List[BannerResponse]