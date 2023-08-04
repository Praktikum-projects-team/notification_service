from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import rabbit_conf
from db.db_session import get_scheduled_events
from event_queue.events_inserting import SyncRabbitPublisher

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    rabbit = SyncRabbitPublisher(
        host=rabbit_conf.host_name,
        port=rabbit_conf.port,
        username=rabbit_conf.user_name,
        password=rabbit_conf.password,
    )

    for event in get_scheduled_events():
        scheduler.add_job(
            rabbit.publish_events(),
            CronTrigger.from_crontab(event.cron_string),
            [event.event_id, event.users, rabbit_conf.queue_name]
        )
    scheduler.print_jobs()
    scheduler.start()
    rabbit.close_connection()
