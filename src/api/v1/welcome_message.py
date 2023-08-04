from fastapi import APIRouter, Depends
import requests

from services.auth import AuthApi
from api.v1.auth.auth_bearer import BaseJWTBearer
from services.notification import NotificationService, get_notification_service

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/{short_link}',
    dependencies=[Depends(BaseJWTBearer())]
)
async def redirect_with_short_link(short_link: str,
                                   notification_service: NotificationService = Depends(get_notification_service)):
    link, params = await notification_service.get_welcome_msg_info(short_link)
    resp = requests.post(link, json=params)
    return resp.json()


@router.get(
    '/test/{user_id}',
    dependencies=[Depends(BaseJWTBearer())]
)
async def test(user_id: str,
               notification_service: NotificationService = Depends(get_notification_service)):
    link = await notification_service.make_short_link(user_id)
    return link
