from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_db
from src.services.auth import AuthApi
from src.services.notification import NotificationService, get_notification_service
from src.api.v1.models.notification import ServiceNotificationRequest

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
    await notification_service.publish_event(data)
