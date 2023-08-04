from typing import Generator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db.models import EventScheduled
from config import PostgresConfig

engine = create_engine(PostgresConfig().dsn)


def get_scheduled_events():
    with Session(engine) as session:
        # stmt = select(EventScheduled).where(EventScheduled.is_active=True)
        stmt = select(EventScheduled)
        for event in session.scalars(stmt):
            yield event
