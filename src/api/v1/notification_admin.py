from fastapi import APIRouter, Depends

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.notification_admin import AllNotificationAdminResp, AddNotificationAdmin, AddNotificationAdminResp
from services.auth import AuthApi
from services.notification_admin import NotificationAdminService, get_notification_admin_service

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/',
    response_model=AddNotificationAdminResp,
    description='Добавление уведомления',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_notification_admin(
        data: AddNotificationAdmin,
        notification_admin_service: NotificationAdminService = Depends(get_notification_admin_service)
) -> AddNotificationAdminResp:
    await notification_admin_service.post_notification(data)

    return AddNotificationAdminResp(msg="Notification added")


@router.get(
    '/',
    response_model=AllNotificationAdminResp,
    description='Получение списка всех уведомлений',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_notification_admin(
        notification_admin_service: NotificationAdminService = Depends(get_notification_admin_service)
) -> AllNotificationAdminResp:
    all_events = await notification_admin_service.get_all_notifications()

    return AllNotificationAdminResp(events=all_events)
