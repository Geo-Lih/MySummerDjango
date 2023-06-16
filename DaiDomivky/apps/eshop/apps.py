from django.apps import AppConfig


class EshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.eshop'

    def ready(self, *args, **kwargs):
        from . import signals
