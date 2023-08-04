from enum import Enum
from uuid import UUID

from pydantic import Field

from core.base_model import OrjsonBaseModel


class Channel(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventCreate(OrjsonBaseModel):
    description: str
    is_unsubscribeable: bool


class EventScheduledCreate(OrjsonBaseModel):
    event_id: UUID
    cron_string: str


class EventUpdate(OrjsonBaseModel):
    description: str
    is_unsubscribeable: bool
    cron_string: str


class EventResp(OrjsonBaseModel):
    id: UUID
    description: str
    is_unsubscribeable: bool
    cron_string: str


class EventWithScheduledResp(OrjsonBaseModel):
    id: UUID
    description: str
    is_unsubscribeable: bool
    cron_string: str


class AllEventsWithScheduledResp(OrjsonBaseModel):
    events: list[EventWithScheduledResp] = Field(default_factory=list)
