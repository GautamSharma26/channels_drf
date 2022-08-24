import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')

# app =Celery('celery_task',
#             broker='amqp://',
#             include=['celery_task.tasks'])

app = Celery('pizza')


app.conf.update(timezone='Asia/Kolkata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     'send-mail-everyday': {
#         'task': 'accounts.task.send_mail_func',
#         'schedule': crontab(hour=18, minute=46),  # day_of_month,month_of_year
#     }
# }

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
