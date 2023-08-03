from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aio_pika import connect, Message, Connection, Channel, Exchange
import orjson
from typing import Optional

from core.config import rm_config
from db.postgres import get_db, get_event_by_id


class EventNotFound(Exception):
    ...


class RabbitPublisher:
    def __init__(self):
        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None
        self.exchange: Optional[Exchange] = None

    async def connect(self):
        self.connection = await connect(rm_config.rabbit_connection)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(rm_config.rm_exchange)

    async def put_event_to_queue(self, event_data, queue_name: str):
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

    async def put_one(self, event_data):
        if await self.check_event(event_data.event_id):
            await self.publisher.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)
        else:
            raise EventNotFound('Event not found')

    async def put_many(self, event_data, users):
        for user in users:
            if await self.check_event(event_data.event_id):
                event_data.user_id = user
                await self.publisher.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)
            else:
                raise EventNotFound('Event not found')

    async def check_event(self, event_id):
        event = await get_event_by_id(event_id, self.session)
        if event:
            return True
        else:
            return False

    async def publish_event(self, event_data):
        receiver = event_data.user_id
        try:
            if isinstance(receiver, list):
                await self.put_many(event_data, receiver)
                return {'msg': 'Notifications for each user from the list have been added to the instant queue'}
            else:
                await self.put_one(event_data)
                return {'msg': 'Notification for user has been added to the instant queue'}
        except EventNotFound:
            raise


notification_service: NotificationService = NotificationService()


@lru_cache()
def get_notification_service() -> NotificationService:
    return notification_service
