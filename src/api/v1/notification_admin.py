from fastapi import APIRouter, Depends

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.notification_admin import NotificationAdmin, NotificationAdminResp
from services.auth import AuthApi
from services.notification_admin import NotificationAdminService, get_notification_admin_service

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/',
    response_model=NotificationAdminResp,
    description='Добавление уведомления в базу данных',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_notification_admin(
        data: NotificationAdmin,
        notification_admin_service: NotificationAdminService = Depends(get_notification_admin_service)
) -> NotificationAdminResp:
    await notification_admin_service.post_notification(data)

    return NotificationAdminResp(msg="Notification added")
