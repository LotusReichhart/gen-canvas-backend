from src.core.model.user.user import User

from ..database.model.user_entity import UserEntity

from .user_credit_mapper import UserCreditMapper


class UserMapper:
    @staticmethod
    def to_model(user_entity: UserEntity) -> User:
        user_credit = None
        if "user_credit" in user_entity.__dict__:
            if user_entity.user_credit:
                user_credit = UserCreditMapper.to_model(user_entity.user_credit)

        return User(
            id=user_entity.id,
            name=user_entity.name,
            email=user_entity.email,
            password=user_entity.password,
            avatar=user_entity.avatar,
            last_login=user_entity.last_login,
            signin_count=user_entity.signin_count,
            sign_out_count=user_entity.sign_out_count,
            status=user_entity.status,
            tier=user_entity.tier,
            auth_provider=user_entity.auth_provider,
            user_credit=user_credit
        )

    @staticmethod
    def to_entity(user: User) -> UserEntity:
        return UserEntity(
            name=user.name,
            email=user.email,
            password=user.password,
            avatar=user.avatar,
            last_login=user.last_login,
            status=user.status,
            tier=user.tier,
            auth_provider=user.auth_provider,
            signin_count=user.signin_count,
            sign_out_count=user.sign_out_count,
        )

    @staticmethod
    def to_update_entity(entity: UserEntity, user: User) -> None:
        entity.name = user.name
        entity.avatar = user.avatar
        entity.last_login = user.last_login
        entity.status = user.status
        entity.tier = user.tier
        entity.signin_count = user.signin_count
        entity.sign_out_count = user.sign_out_count

        if entity.password is not None:
            entity.password = user.password
