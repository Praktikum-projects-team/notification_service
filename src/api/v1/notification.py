from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from services.auth import AuthApi
from services.notification import NotificationService, get_notification_service, EventNotFound
from api.v1.models.notification import ServiceNotificationRequest

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/template',
)
async def get_notification_template(session: AsyncSession=Depends(get_db)):
    pass


@router.post(
    '/admin',
)
async def add_notification_admin():
    pass


@router.post(
    '/service',
    description='Отправка уведомлений от других сервисов в очередь'
)
async def add_notification_service(data: ServiceNotificationRequest,
                                   notification_service: NotificationService = Depends(get_notification_service)):
    try:
        return await notification_service.publish_event(data)
    except EventNotFound as err:
        return {'msg': str(err)}, HTTPStatus.NOT_FOUND
