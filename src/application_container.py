from dependency_injector import containers, providers
from src.config.settings import settings
from src.core.data.database.di.database_container import DatabaseContainer
from src.core.data.external_service.di.external_service_container import ExternalServiceContainer
from src.core.data.repository.di.repository_container import RepositoryContainer
from src.core.data.service.di.service_container import ServiceContainer
from src.core.domain.usecase.di.usecase_container import UseCaseContainer


class ApplicationContainer(containers.DeclarativeContainer):
    # Wiring Config
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.presentation.v1",
            "src.presentation.webhooks",
        ]
    )

    config = providers.Configuration()
    config.from_pydantic(settings)

    # 1. Database
    database_package = providers.Container(
        DatabaseContainer,
        config=config
    )

    # 2. External service (Redis, S3, Mail...)
    external_service_package = providers.Container(
        ExternalServiceContainer,
        config=config
    )

    # 3. Repository
    repository_package = providers.Container(
        RepositoryContainer,
        database_container=database_package
    )

    # 4. Service
    service_package = providers.Container(
        ServiceContainer,
        config=config,
        external_service_container=external_service_package
    )

    # 5. UseCases
    use_case_package = providers.Container(
        UseCaseContainer,
        config=config,
        repository_container=repository_package,
        service_container=service_package
    )
