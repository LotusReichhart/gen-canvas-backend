from dependency_injector import containers, providers

from ..postgres import PostgresDatabase


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        PostgresDatabase,
        db_url=config.database_url
    )