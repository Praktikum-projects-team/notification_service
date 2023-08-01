from enum import Enum
from uuid import UUID

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


class EventResponse(OrjsonBaseModel):
    id: UUID
    description: str
    is_unsubscribeable: bool
