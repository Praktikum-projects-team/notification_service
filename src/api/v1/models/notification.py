from uuid import UUID

from src.core.base_model import OrjsonBaseModel


class ServiceNotificationRequest(OrjsonBaseModel):
    user_id: UUID | list
    event_id: str

