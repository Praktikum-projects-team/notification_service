import random
import string
from functools import lru_cache
from uuid import UUID

import orjson
from aio_pika import ExchangeType, Message, connect
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models.notification import ServiceNotificationRequest
from core.config import app_config, rm_config
from db.postgres import get_db, get_event, get_link, insert_short_link


class EventNotFound(Exception):
    ...


class RabbitPublisher:
    def __init__(self, connection=None, channel=None, exchange=None):
        self.connection: AbstractConnection = connection
        self.channel: AbstractChannel = channel
        self.exchange: AbstractExchange = exchange

    async def connect(self):
        self.connection = await connect(rm_config.rabbit_connection)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            name=rm_config.rm_exchange,
            type=ExchangeType.FANOUT,
            durable=True,
        )

    async def put_event_to_queue(self, event_data: ServiceNotificationRequest, queue_name: str):
        msg = Message(body=orjson.dumps(event_data.dict()), delivery_mode=rm_config.rm_delivery_mode)
        queue = await self.channel.declare_queue(name=queue_name)
        await queue.bind(self.exchange)
        await self.exchange.publish(message=msg, routing_key=queue_name)

    async def close_connection(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        self.connection = None
        self.channel = None
        self.exchange = None


class NotificationService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.publisher = RabbitPublisher()
        self.session = session

    async def put_one(self, event_data: ServiceNotificationRequest):
        if not await self.check_event(event_data.event_id):
            raise EventNotFound('Event not found')
        await self.publisher.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)

    async def put_many(self, event_data: ServiceNotificationRequest, users: list):
        if not await self.check_event(event_data.event_id):
            raise EventNotFound('Event not found')

        for user in users:
            event_data.user_id = user
            await self.publisher.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)

    async def check_event(self, event_id: str):
        event = await get_event(self.session, event_id)
        if event:
            return True
        return False

    async def publish_event(self, event_data: ServiceNotificationRequest):
        receiver = event_data.user_id
        try:
            if isinstance(receiver, list):
                await self.put_many(event_data, receiver)
                return {'msg': 'Notifications for each user from the list have been added to the instant queue'}
            await self.put_one(event_data)
            return {'msg': 'Notification for user has been added to the instant queue'}
        except EventNotFound:
            raise

    async def get_welcome_msg_info(self, short_link: str):
        link_data = await get_link(short_link, self.session)
        link_params = {"ttl": str(link_data.ttl), "redirect_link": link_data.redirect_url,
                       "user_id": str(link_data.user_id)}
        return link_data.original_link, link_params

    async def generate_link(self) -> str:
        letters_and_numbs = string.ascii_letters + string.digits
        random_string = ''.join(random.sample(letters_and_numbs, 8))
        return random_string

    async def make_short_link(self, user_id: UUID) -> str:
        generated_link = await self.generate_link()
        await insert_short_link(generated_link, user_id, self.session)
        link = f'http://{app_config.host}:{app_config.port}/api/v1/welcome/{generated_link}'
        return link


@lru_cache()
def get_notification_service(session: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(session=session)
