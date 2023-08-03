from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.notification_admin import AllNotificationAdminResp, AddNotificationAdmin, AddNotificationAdminResp, \
    NotificationAdminResp
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
async def get_all_notifications_admin(
        notification_admin_service: NotificationAdminService = Depends(get_notification_admin_service)
) -> AllNotificationAdminResp:
    all_events = await notification_admin_service.get_all_notifications()

    return AllNotificationAdminResp(events=all_events)


@router.get(
    '/{event_id}',
    response_model=NotificationAdminResp,
    description='Получение одного уведомления',
    dependencies=[Depends(BaseJWTBearer())]
)
async def get_notification_admin(
        event_id: str,
        notification_admin_service: NotificationAdminService = Depends(get_notification_admin_service)
) -> NotificationAdminResp:
    event = await notification_admin_service.get_notification(event_id=event_id)
    if not event:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Notification not found')

    return NotificationAdminResp(**event)
