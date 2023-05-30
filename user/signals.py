from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser
from .tasks import send_registration_email


@receiver(post_save, sender=CustomUser)
def email_processing_completed(sender, instance, created, **kwargs):
    if created:
        send_registration_email.delay(instance.email)
