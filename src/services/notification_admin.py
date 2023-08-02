from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_data import EventCreate, EventScheduledCreate
from db.postgres import get_all_events, get_db, insert_event, insert_event_scheduled


class NotificationAdminService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def post_notification(self, data):
        event_data = EventCreate(description=data.description, is_unsubscribeable=data.is_unsubscribeable)
        event_id = await insert_event(event_data, self.session)

        event_scheduled_data = EventScheduledCreate(event_id=event_id, cron_string=data.cron_string)
        await insert_event_scheduled(event_scheduled_data, self.session)

    async def get_all_notifications(self):
        all_events = await get_all_events(self.session)
        all_events_for_resp = list()

        for event in all_events.events:
            event_dict = {
                'id': str(event.id),
                'description': event.description,
                'is_unsubscribeable': event.is_unsubscribeable,
                'cron_string': event.cron_string
            }
            all_events_for_resp.append(event_dict)

        return all_events_for_resp


@lru_cache()
def get_notification_admin_service(session: AsyncSession = Depends(get_db)) -> NotificationAdminService:
    return NotificationAdminService(session=session)
