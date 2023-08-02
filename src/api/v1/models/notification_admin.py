from uuid import UUID

from pydantic import Field

from core.base_model import OrjsonBaseModel


class NotificationAdmin(OrjsonBaseModel):
    description: str
    is_unsubscribeable: bool = Field(default=False)


class AddNotificationAdminResp(OrjsonBaseModel):
    msg: str


class NotificationAdminResp(OrjsonBaseModel):
    id: UUID
    description: str
    is_unsubscribeable: bool = Field(default=False)


class AllNotificationAdminResp(OrjsonBaseModel):
    events: list[NotificationAdminResp]
