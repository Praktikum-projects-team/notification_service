from functools import lru_cache
from aio_pika import connect, Message
import orjson
from src.core.config import rm_config


class UserNotFound(Exception):
    ...


class EventNotFound(Exception):
    ...


class RabbitPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect_rm(self):
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
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        self.connection = None
        self.channel = None
        self.exchange = None


class NotificationService(RabbitPublisher):
    async def put_one(self, event_data):
        if self.check_user(event_data.user_id) and self.check_event(event_data.event_id):
            await self.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)
        elif self.check_user(event_data.user_id) is False:
            raise UserNotFound('User not found')
        else:
            raise EventNotFound('Event not found')

    async def put_many(self, event_data, users):
        for user in users:
            if self.check_user(user) and self.check_event(event_data.event_id):
                event_data.user_id = user
                await self.put_event_to_queue(event_data, rm_config.rm_instant_queue_name)
            elif self.check_user(user) is False:
                raise UserNotFound('User not found')
            else:
                raise EventNotFound('Event not found')

    async def check_user(self, user_id):
        return True

    async def check_event(self, event_id):
        return True

    async def publish_event(self, event_data):
        receiver = event_data.user_id
        try:
            if isinstance(receiver, list):
                await self.put_many(event_data, receiver)
            else:
                await self.put_one(event_data)
        except (UserNotFound, EventNotFound):
            raise


@lru_cache()
async def get_notification_service() -> NotificationService:
    serv = NotificationService()
    await serv.connect_rm()
    return serv
