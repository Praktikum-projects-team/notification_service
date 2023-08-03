from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.config import pg_config

async_engine = create_async_engine(pg_config.url_async)


async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session


async def get_event_by_id(event_id: str, session):
    pass
