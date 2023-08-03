import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db.models_data import Channel


if TYPE_CHECKING:
    class Base:
        pass
else:
    Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    is_unsubscribeable = Column(Boolean)


class Template(Base):
    __tablename__ = 'templates'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    template = Column(String)


class NotificationTemplate(Base):
    __tablename__ = 'notification_templates'
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True)
    channel: Channel = Column(Enum(Channel))
    template_id = Column(UUID(as_uuid=True), ForeignKey('templates.id'))
    event = relationship('Event')
    template = relationship('Template')


class UserUnsubscribed(Base):
    __tablename__ = 'users_unsubscribed'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    channel: Channel = Column(Enum(Channel))


class EventScheduled(Base):
    __tablename__ = 'events_scheduled'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'))
    cron_string = Column(String)


class ScheduledEventUser(Base):
    __tablename__ = 'scheduled_events_users'
    scheduled_event_id = Column(UUID(as_uuid=True), ForeignKey('events_scheduled.id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True))


class NotificationSent(Base):
    __tablename__ = 'notifications_sent'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'))
    delivery_dt = Column(DateTime)
