from http import HTTPStatus

from fastapi import APIRouter, Depends

from api.v1.models.notification import ServiceNotificationRequest
from services.auth import AuthApi
from services.notification import EventNotFound, NotificationService, get_notification_service

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/service',
    description='Отправка уведомлений от других сервисов в очередь'
)
async def add_notification_service(
        data: ServiceNotificationRequest,
        notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        return await notification_service.publish_event(data)
    except EventNotFound as err:
        return {'msg': str(err)}, HTTPStatus.NOT_FOUND
