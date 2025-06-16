from __future__ import absolute_import
import os
from celery import Celery
import asyncio
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('course_work_5')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'habits.tasks.send_reminders',
        'schedule': crontab(minute='*/2'),
    },
}
