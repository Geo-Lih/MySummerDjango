from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .tasks import send_is_published_email


@receiver(post_save, sender=Post)  # listener
def post_is_published(sender, instance, created, **kwargs):
    if instance.status == 1:
        send_is_published_email.delay(instance.id)
