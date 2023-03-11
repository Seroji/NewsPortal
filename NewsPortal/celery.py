import os
from celery import Celery, schedules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('content')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'content.tasks.every_week_sending',
        'schedule': schedules.crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
