import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from core.config import auth_config
from db.models_data import Channel

if TYPE_CHECKING:
    class Base:
        pass
else:
    Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(150))
    is_unsubscribeable = Column(Boolean, nullable=False, default=False)


class EventScheduled(Base):
    __tablename__ = 'events_scheduled'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    cron_string = Column(String(200), nullable=False)


class ScheduledEventUser(Base):
    __tablename__ = 'scheduled_events_users'
    scheduled_event_id = Column(
        UUID(as_uuid=True),
        ForeignKey('events_scheduled.id', ondelete='CASCADE'),
        primary_key=True
    )
    user_id = Column(UUID(as_uuid=True), primary_key=True)


class Template(Base):
    __tablename__ = 'templates'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(100))
    template = Column(Text, nullable=False)
    title = Column(String(50))


class NotificationTemplate(Base):
    __tablename__ = 'notification_templates'
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), primary_key=True)
    channel: Channel = Column(Enum(Channel), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)

    event = relationship('Event')
    template = relationship('Template')


class UserUnsubscribed(Base):
    __tablename__ = 'users_unsubscribed'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    channel: Channel = Column(Enum(Channel), nullable=False)


class NotificationSent(Base):
    __tablename__ = 'notifications_sent'
    user_id = Column(UUID(as_uuid=True), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    delivery_dt = Column(DateTime, nullable=False)


class ShortLinks(Base):
    __tablename__ = 'short_links'
    short_link = Column(String(20), primary_key=True)
    original_link = Column(String(250), default=auth_config.url_verify, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    ttl = Column(DateTime, nullable=False, default=datetime.utcnow)
    redirect_url = Column(String(250), default=auth_config.url_redirect)
