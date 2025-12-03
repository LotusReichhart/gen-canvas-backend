from typing import Optional

from pydantic import BaseModel, ConfigDict


class Banner(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: Optional[str] = None
    image_url: str
    action_url: Optional[str] = None
    display_order: int
    is_active: bool = True
