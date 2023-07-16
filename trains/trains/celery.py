import os

from celery import Celery
from celery.schedules import crontab
from .settings import TIME_ZONE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trains.settings')

app = Celery('trains')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = TIME_ZONE
app.conf.beat_schedule = {
    'get_routes_and_tickets_from_api': {
        'task': 'data.tasks.get_routes_and_tickets_from_api',
        'schedule': crontab(minute=0, hour=0)
    }
}