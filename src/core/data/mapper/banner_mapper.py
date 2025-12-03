from src.core.model.banner import Banner

from ..database.model.banner_entity import BannerEntity


class BannerMapper:
    @staticmethod
    def to_model(banner_entity: BannerEntity) -> Banner:
        return BannerEntity(
            id=banner_entity.id,
            title=banner_entity.title,
            image_url=banner_entity.image_url,
            action_url=banner_entity.action_url,
            display_order=banner_entity.display_order,
            is_active=banner_entity.is_active
        )

    @staticmethod
    def to_entity(banner: Banner) -> BannerEntity:
        return BannerEntity(
            title=banner.title,
            image_url=banner.image_url,
            action_url=banner.action_url,
            display_order=banner.display_order,
            is_active=banner.active,
        )
