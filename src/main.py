import logging
from http import HTTPStatus
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from httpx import RequestError

from api.v1 import notification
from api.v1 import welcome_message
from core.logger import LOGGING
from core.config import app_config
from services.notification import notification_service, RabbitPublisher

from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit_publisher = RabbitPublisher()
    await rabbit_publisher.connect()
    notification_service.publisher = rabbit_publisher
    yield
    await rabbit_publisher.close_connection()


app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(notification.router, prefix='/api/v1/notification', tags=['notification'])
app.include_router(welcome_message.router, prefix='/api/v1/welcome', tags=['welcome_message'])


@app.exception_handler(RequestError)
async def bad_storage_request_exception_handler(request, exc):
    http_exc = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.error)
    return await http_exception_handler(request, http_exc)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )
