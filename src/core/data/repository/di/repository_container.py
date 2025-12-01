from dependency_injector import containers, providers

from src.core.domain.repository.unit_of_work import UnitOfWork

from ..unit_of_work_impl import UnitOfWorkImpl


class RepositoryContainer(containers.DeclarativeContainer):
    database_container = providers.DependenciesContainer()

    unit_of_work: UnitOfWork = providers.Factory(
        UnitOfWorkImpl,
        db=database_container.db
    )
