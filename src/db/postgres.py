import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import exc as orm_exc
import datetime

from core.config import pg_config
from db.models_pg import ShortLinks

async_engine = create_async_engine(pg_config.url_async)


async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session


async def get_event_by_id(event_id: str, session):
    pass


async def insert_short_link(link: str, user_id, session: AsyncSession):
    try:
        ttl = datetime.datetime.utcnow() + datetime.timedelta(1)
        short_link_data = ShortLinks(short_link=link, user_id=user_id, ttl=ttl)
        session.add(short_link_data)
        await session.commit()
        await session.refresh(short_link_data)
    except Exception as e:
        await session.rollback()
        logging.error(e)
        return None


async def get_link(short_link: str, session):
    try:
        query = select(ShortLinks).filter(ShortLinks.short_link == short_link)
        result = await session.execute(query)
        link = result.scalar_one()

        return link

    except orm_exc.NoResultFound:
        return None

    except Exception as e:
        logging.warning(e)
        return None
