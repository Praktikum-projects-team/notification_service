from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from db.db_session import get_scheduled_events
from event_queue.events_inserting import post_event_to_queue

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    for event in get_scheduled_events():
        scheduler.add_job(
            post_event_to_queue,
            CronTrigger.from_crontab(event.cron_string),
            [event.event_id, event.users]
        )
    scheduler.print_jobs()
    scheduler.start()
