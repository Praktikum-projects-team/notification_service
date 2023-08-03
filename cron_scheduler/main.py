from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = BlockingScheduler()

scheduler.add_job(job_function, CronTrigger.from_crontab('* 15 * may-aug *'))
scheduler.add_job(job_function2, CronTrigger.from_crontab('* 15 * may-aug *'))

print('start')
scheduler.start()