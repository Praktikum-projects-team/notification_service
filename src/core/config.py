import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    is_debug: bool = Field(..., env='IS_DEBUG')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')


class PostgresConfig(BaseSettings):
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    name: str = Field(..., env='POSTGRES_DB')

    @property
    def url_sync(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @property
    def url_async(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


app_config = AppConfig()  # type: ignore[call-arg]
auth_config = AuthConfig()  # type: ignore[call-arg]
pg_config = PostgresConfig()  # type: ignore[call-arg]
