import uuid

import orjson
import pika


class SyncRabbitPublisher:
    def __init__(self, host: str, port: int, username: str, password: str):
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username=username, password=password),
        )
        self.connection = pika.BlockingConnection(parameters)

    def publish_events(self, event: uuid.UUID, users: list, queue: str):
        with self.connection.channel() as channel:
            body = {'event_id': event}
            for user in users:
                body['user_id'] = user.id
                channel.basic_publish(
                    exchange=queue + '_exchange',
                    routing_key=queue,
                    body=orjson.dumps(body),
                )

    def close_connection(self):
        self.connection.close()
