from pydantic import BaseSettings, Field


class RabbitMQ(BaseSettings):
    host_name: str = Field('127.0.0.1', env='RABBITMQ_HOST_NAME')
    user_name: str = Field('guest', env='RABBITMQ_DEFAULT_USER')
    password: str = Field('guest', env='RABBITMQ_DEFAULT_PASS')
    port: int = Field(5672, env='RABBITMQ_PORT')
    queue_name: str = Field('first', env='RABBITMQ_QUEUE_NAME')


class Settings(BaseSettings):
    rabbit_mq: RabbitMQ = RabbitMQ()
    # auth_api: str

    class Config:
        env_file = '.env'