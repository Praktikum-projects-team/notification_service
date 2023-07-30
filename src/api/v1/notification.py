from fastapi import APIRouter, Depends, Request, HTTPException
from http import HTTPStatus
from services.auth import AuthApi

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/template',
)
async def get_notification_template():
    pass


@router.post(
    '/admin',
)
async def add_notification_admin():
    pass


@router.post(
    '/service',
)
async def add_notification_service():
    pass
