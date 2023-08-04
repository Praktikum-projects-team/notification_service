from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    name: str = Field(..., env='POSTGRES_DB')

    @property
    def dsn(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    class Config:
        env_file = '.env'


class RabbitMQ(BaseSettings):
    host_name: str = Field('127.0.0.1', env='RABBITMQ_HOST_NAME')
    user_name: str = Field('guest', env='RABBITMQ_DEFAULT_USER')
    password: str = Field('guest', env='RABBITMQ_DEFAULT_PASS')
    port: int = Field(5672, env='RABBITMQ_PORT')
    queue_name: str = Field(env='RABBITMQ_SCHEDULED_QUEUE')

    class Config:
        env_file = '.env'


rabbit_conf = RabbitMQ()
