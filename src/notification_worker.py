import asyncio
import logging
from uuid import UUID

import sqlalchemy as sa
from aio_pika.abc import AbstractIncomingMessage
from pydantic import parse_raw_as
from sqlalchemy.orm import selectinload

from core.config import rm_config
from db.models_data import UserNotification
from db.models_pg import Event, NotificationTemplate, UserUnsubscribed
from db.postgres import AsyncSession, async_engine
from db.rabbit import get_rabbit
from services.auth import get_auth_api
from services.notification_channels import NOTIFICATION_CHANNELS

logger = logging.getLogger(__name__)


async def callback(message: AbstractIncomingMessage):
    try:
        user_notification = parse_raw_as(UserNotification, message.body)
        user_info = await get_auth_api().get_user_info(user_notification.user_id)
        if user_info is None:
            return

        templates = await get_templates(
            user_id=user_notification.user_id,
            event_id=user_notification.event_id,
        )
        if templates is None or len(templates) == 0:
            return

        templates_by_channel = {template.channel: template for template in templates}
        for channel, template in templates_by_channel.items():
            if notification_channel := NOTIFICATION_CHANNELS.get(channel):
                await notification_channel.send(
                    email=user_info.login,
                    title=template.template.title,
                    template=template.template.template,
                    **user_notification.additional_data,
                )

        await message.ack()
    except Exception as e:
        logger.exception(e)


async def get_templates(user_id: UUID, event_id: UUID):
    async with AsyncSession(async_engine) as session:
        # fmt: off
        statement = (
            sa.select(UserUnsubscribed)
            .where(UserUnsubscribed.user_id == user_id)
        )
        # fmt: on
        result = await session.execute(statement)
        user_unsubscribed = result.scalars().fetchall()
        user_unsubscribed_channels = {user.channel for user in user_unsubscribed}
        statement = (
            sa.select(NotificationTemplate)
            .join(NotificationTemplate.event)
            .join(NotificationTemplate.template)
            .where(
                sa.and_(
                    Event.id == event_id,
                    NotificationTemplate.channel.not_in(user_unsubscribed_channels),  # type: ignore
                )
            )
            .options(
                selectinload(NotificationTemplate.event),
                selectinload(NotificationTemplate.template),
            )
        )
        result = await session.execute(statement)
        return result.scalars().fetchall()


async def main():
    connection, queue = await get_rabbit(
        exchange_name=rm_config.rm_exchange,
        queue_name=rm_config.rm_instant_queue_name,
    )
    await queue.consume(callback)
    logger.info('Start consumming...')

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == '__main__':
    asyncio.run(main())
