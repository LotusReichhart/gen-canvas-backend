from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..postgres import Base


class BannerEntity(Base):
    __tablename__ = 'banners'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(unique=True, index=True)
    action_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    display_order: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
