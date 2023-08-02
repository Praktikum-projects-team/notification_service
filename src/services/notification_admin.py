from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_data import EventCreate, EventScheduledCreate
from db.postgres import get_all_events, get_db, insert_event, insert_event_scheduled


class NotificationAdminService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def post_notification(self, data):
        event_data = EventCreate(**data.dict())
        event_id = await insert_event(event_data, self.session)

        event_scheduled_data = EventScheduledCreate(event_id=event_id, cron_string='0 17 1')
        await insert_event_scheduled(event_scheduled_data, self.session)

    async def get_all_notifications(self):
        all_events = await get_all_events(self.session)
        return all_events


@lru_cache()
def get_notification_admin_service(session: AsyncSession = Depends(get_db)) -> NotificationAdminService:
    return NotificationAdminService(session=session)
