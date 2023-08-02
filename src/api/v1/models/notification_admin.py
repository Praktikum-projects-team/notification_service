from uuid import UUID

from pydantic import Field

from core.base_model import OrjsonBaseModel


class AddNotificationAdmin(OrjsonBaseModel):
    description: str
    is_unsubscribeable: bool = Field(default=False)
    cron_string: str


class AddNotificationAdminResp(OrjsonBaseModel):
    msg: str


class NotificationAdminResp(OrjsonBaseModel):
    id: UUID
    description: str
    is_unsubscribeable: bool = Field(default=False)
    cron_string: str


class AllNotificationAdminResp(OrjsonBaseModel):
    events: list[NotificationAdminResp] = Field(default_factory=list)
