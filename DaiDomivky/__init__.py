# Django is using this .py file to init the proj. Importing 'celery_app' guarantees ->
# -> that Celery will be loaded and ready for use as soon as Django starts working

from .celery import app as celery_app

__all__ = ('celery_app',)
