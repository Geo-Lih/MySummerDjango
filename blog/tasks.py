from user.models import CustomUser

from celery import group, shared_task

from django.core.mail import send_mail

from .models import Post


@shared_task()
def send_is_published_email(post_title):
    users_email = CustomUser.objects.values_list('email', flat=True)  # flat=True to avoid tuples'

    # creating group tasks based on lower func
    group(send_email_to_user.s(post_title, user_email) for user_email in users_email)()


@shared_task()
def send_email_to_user(post_title, user_email):
    print(post_title, user_email)
    send_mail(
        f'New Post: {post_title}',
        f'Post {post_title} was published.',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )
