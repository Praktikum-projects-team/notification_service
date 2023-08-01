import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import exc as orm_exc

from core.config import pg_config
from db.models_data import EventCreate, EventResponse, EventScheduledCreate
from db.models_pg import Event, EventScheduled

async_engine = create_async_engine(pg_config.url_async)


async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session


async def get_event_by_id(event_id: str, session):
    try:
        query = select(Event).filter(Event.id == event_id)
        result = await session.execute(query)
        event = result.scalar_one()
        return EventResponse(**event.dict())

    except orm_exc.NoResultFound:
        return None

    except Exception as e:
        logging.warning(e)
        return None


async def insert_event(event_data: EventCreate, session):
    try:
        event = Event(**event_data.dict())
        session.add(event)
        await session.commit()
        await session.refresh(event)
        logging.info(f'event.id: {event.id}')
        return event.id

    except IntegrityError as e:
        session.rollback()
        logging.info('Event already exists')
        return None

    except Exception as e:
        session.rollback()
        logging.error(e)
        return None


async def insert_event_scheduled(event_scheduled_data: EventScheduledCreate, session):
    try:
        event_scheduled = EventScheduled(**event_scheduled_data.dict())
        session.add(event_scheduled)
        await session.commit()
        session.refresh(event_scheduled)
        return event_scheduled.id

    except Exception as e:
        logging.error(e)
        return None
