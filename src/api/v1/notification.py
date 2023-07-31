from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from services.auth import AuthApi

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
)
async def add_notification_service():
    pass
