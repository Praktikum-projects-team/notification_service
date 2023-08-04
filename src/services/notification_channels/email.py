import logging
import smtplib
from email.message import EmailMessage

from core.config import smtp_config
from db.models_data import Channel

from .base import BaseNotificationChannel

logger = logging.getLogger(__name__)


class EmailNotificationChannel(BaseNotificationChannel):
    type = Channel.email

    async def send(self, email: str, title: str, template: str, **kwargs):
        try:
            msg = EmailMessage()
            msg['Subject'] = title
            msg['From'] = smtp_config.email
            msg['To'] = email
            msg.set_content(self._render_template(template, **kwargs))

            with smtplib.SMTP_SSL(smtp_config.host, smtp_config.port) as smtp:
                smtp.login(smtp_config.email, smtp_config.password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            logger.exception(e)
            return False
