from uuid import UUID
from typing import Union

from core.base_model import OrjsonBaseModel


class ServiceNotificationRequest(OrjsonBaseModel):
    user_id: Union[UUID, list]
    event_id: str
