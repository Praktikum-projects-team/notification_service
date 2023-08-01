from pydantic import Field

from core.base_model import OrjsonBaseModel


class NotificationAdmin(OrjsonBaseModel):
    description: str
    is_unsubscribeable: bool = Field(default=False)


class NotificationAdminResp(OrjsonBaseModel):
    msg: str
