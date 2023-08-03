import logging

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import exc as orm_exc

from core.config import pg_config
from db.models_data import (
    AllEventsWithScheduledResp,
    EventCreate,
    EventResp,
    EventScheduledCreate,
    EventUpdate
)
from db.models_pg import Event, EventScheduled

async_engine = create_async_engine(pg_config.url_async)


async def get_db():
    async with AsyncSession(async_engine) as session:
        yield session


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
        await session.refresh(event_scheduled)
        return event_scheduled.id

    except Exception as e:
        logging.error(e)
        return None


async def get_all_events(session):
    try:
        events = await session.execute(select(Event))
        all_events = events.scalars().all()
        formatted_events_all = list()

        for event in all_events:
            event_scheduled = await session.execute(
                select(EventScheduled.cron_string)
                .where(EventScheduled.event_id == event.id)
                .limit(1)
            )
            cron_string = event_scheduled.scalar_one_or_none()
            formatted_event = {
                # **event.__dict__,
                'id': str(event.id),
                'description': event.description,
                'is_unsubscribeable': event.is_unsubscribeable,
                'cron_string': cron_string
            }

            formatted_events_all.append(formatted_event)

        return AllEventsWithScheduledResp(events=formatted_events_all)

    except Exception as e:
        logging.error(e)
        return None


async def get_event_by_id(session, event_id: str):
    try:
        query = select(Event).filter(Event.id == event_id)
        result = await session.execute(query)
        event = result.scalar_one()

        event_scheduled = await session.execute(
            select(EventScheduled.cron_string)
            .where(EventScheduled.event_id == event_id)
            .limit(1)
        )

        cron_string = event_scheduled.scalar_one_or_none()
        formatted_event = {
            'id': str(event.id),
            'description': event.description,
            'is_unsubscribeable': event.is_unsubscribeable,
            'cron_string': cron_string
        }

        return EventResp(**formatted_event)

    except orm_exc.NoResultFound:
        return None

    except Exception as e:
        logging.warning(e)
        return None


async def put_event_by_id(session, event_id: str, event_data: EventUpdate):
    try:
        event_query = (
            update(Event)
            .where(Event.id == event_id)
            .values(description=event_data.description, is_unsubscribeable=event_data.is_unsubscribeable)
        )
        await session.execute(event_query)

        event_scheduled_query = (
            update(EventScheduled)
            .where(EventScheduled.event_id == event_id)
            .values(cron_string=event_data.cron_string)
        )
        await session.execute(event_scheduled_query)
        await session.commit()

        return True

    except Exception as e:
        logging.error(e)
        return None
