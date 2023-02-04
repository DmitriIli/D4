import os
from celery import Celery
from celery.schedules import crontab

# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_second': {
        'task': 'news.tasks.weekly_notify',  # задача
        'schedule': crontab(minute='0', hour='0', day_of_week='1'),
        'args': ()
    },
}