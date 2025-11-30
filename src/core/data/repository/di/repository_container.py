from dependency_injector import containers, providers

from ..banner_repository_impl import BannerRepositoryImpl
from ..credit_transaction_repository_impl import CreditTransactionRepositoryImpl
from ..unit_of_work_impl import UnitOfWorkImpl
from ..user_credit_repository_impl import UserCreditRepositoryImpl
from ..user_repository_impl import UserRepositoryImpl


class RepositoryContainer(containers.DeclarativeContainer):
    database_container = providers.DependenciesContainer()

    user_repository = providers.Factory(
        UserRepositoryImpl,
        db=database_container.db
    )

    user_credit_repository = providers.Factory(
        UserCreditRepositoryImpl,
        db=database_container.db
    )

    credit_transaction_repository = providers.Factory(
        CreditTransactionRepositoryImpl,
        db=database_container.db
    )

    banner_repository = providers.Factory(
        BannerRepositoryImpl,
        db=database_container.db
    )

    unit_of_work = providers.Factory(
        UnitOfWorkImpl,
        db=database_container.db
    )
