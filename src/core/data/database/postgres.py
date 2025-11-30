from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PostgresDatabase:
    def __init__(self, db_url: str):
        self._engine = create_async_engine(
            db_url,
            echo=False,
            future=True
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @property
    def session_factory(self):
        return self._session_factory

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_database(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)