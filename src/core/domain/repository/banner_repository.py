from abc import ABC, abstractmethod
from typing import List

from src.core.model.user.banner import Banner


class BannerRepository(ABC):
    @abstractmethod
    async def list_active_banners(self) -> List[Banner]:
        raise NotImplementedError
