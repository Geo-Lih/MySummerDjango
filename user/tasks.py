from celery import shared_task

from django.core.mail import send_mail


@shared_task()  # links to celery with which django was launched(current)
def send_registration_email(email):
    send_mail(
        'Welcome',
        'You have successfully registered.',
        'from@example.com',
        [email],
        fail_silently=False,
    )
