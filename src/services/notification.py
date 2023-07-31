from functools import lru_cache

from fastapi import Depends


class NotificationService:
    def __init__(self, pg):
        self.pg_db = pg


@lru_cache()
def get_notification_service() -> NotificationService:
    pg = None
    return NotificationService(pg)
