from dependency_injector import containers, providers
from src.config.settings import settings
from src.core.data.database.di.database_container import DatabaseContainer
from src.core.data.repository.di.repository_container import RepositoryContainer
from src.core.domain.usecase.di.usecase_container import UseCaseContainer


class ApplicationContainer(containers.DeclarativeContainer):
    # Wiring Config
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.controllers.user_controller",
            "src.presentation.controllers.auth_controller",
        ]
    )

    config = providers.Configuration()
    config.from_pydantic(settings)

    # 1. Database
    database_package = providers.Container(
        DatabaseContainer,
        config=config
    )

    # 2. Gateways (Redis, S3, Mail...)
    # gateways_package = providers.Container(
    #     GatewaysContainer,
    #     config=config
    # )

    # 3. Repository
    repository_package = providers.Container(
        RepositoryContainer,
        database_container=database_package
    )

    # 4. UseCases (Đã đổi tên package cho tường minh)
    use_case_package = providers.Container(
        UseCaseContainer,
        repository_container=repository_package,
        # gateways_container=gateways_package
    )