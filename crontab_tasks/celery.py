from celery import Celery
from celery.schedules import crontab
import os
"""
Refer to https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules

"""
app = Celery('crontab_tasks',
             include=['crontab_tasks.tasks'])
app.config_from_object('crontab_tasks.celeryconfig')

app.conf.beat_schedule = {


    "periodically_request_available_labs_report": {
        "task":'crontab_tasks.tasks.periodically_request_available_labs_report',
        "schedule": crontab(minute=int(os.environ.get('request_frequency',"*/2")))
    }
}