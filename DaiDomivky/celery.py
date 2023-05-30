import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DaiDomivky.settings')  # not required for using it from shell

app = Celery('DaiDomivky')  # creating new instance of Celery with such name

app.config_from_object('django.conf:settings', namespace='CELERY')
# all Celery settings are starting with CELERY_ pref

app.conf.task_send_sent_event = True  # Enable task events
app.conf.update(task_track_started=True)

app.autodiscover_tasks()  # to define tasks in 'tasks.py' from all registered Django apps
