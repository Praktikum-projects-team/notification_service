import uuid

import orjson
import pika

from db.models import ScheduledEventUser


class SyncRabbitPublisher:
    def __init__(self, host: str, port: int, username: str, password: str):
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username=username, password=password),
        )
        self.connection = pika.BlockingConnection(parameters)

    def publish_events(self, event: uuid.UUID, users: list[ScheduledEventUser], queue: str):
        body = {'event_id': event}
        for user in users:
            body['user_id'] = user.user_id
            self.connection.channel().basic_publish(
                exchange=queue,
                routing_key=queue,
                body=orjson.dumps(body),
            )

    def close_connection(self):
        self.connection.close()
