import logging
from abc import ABC, abstractmethod

from jinja2 import BaseLoader, Environment

from db.models_data import Channel

logger = logging.getLogger(__name__)


class BaseNotificationChannel(ABC):
    type: Channel

    @abstractmethod
    async def send(self, email: str, title: str, template: str, **kwargs):
        ...

    def _render_template(self, template: str, **kwargs):
        raw_template = Environment(loader=BaseLoader()).from_string(template)
        return raw_template.render(**kwargs)
