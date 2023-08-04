import uuid

from sqlalchemy import DateTime, Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class EventScheduled(Base):
    __tablename__ = 'events_scheduled'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    event_id = Column(UUID(as_uuid=True))
    cron_string = Column(String)

    users = relationship('ScheduledEventUser')

    def __repr__(self) -> str:
        ...
        return f"EVS(id={self.id!r}, event={self.event_id!r}, cron={self.cron_string!r}, users={self.users!r}, )"


class ScheduledEventUser(Base):
    __tablename__ = 'scheduled_events_users'
    scheduled_event_id = Column(UUID(as_uuid=True), ForeignKey('events_scheduled.id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), primary_key=True)