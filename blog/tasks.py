from user.models import CustomUser

from celery import group, shared_task

from django.core.mail import send_mail

from .models import Post


@shared_task()
def send_is_published_email(post_id):  # post_id => post.id

    users = CustomUser.objects.all()

    group(send_email_to_user.s(post_id, user.id) for user in users)()  # creating group tasks based on lower func


@shared_task()
def send_email_to_user(post_id, user_id):
    post = Post.objects.get(id=post_id)  # getting needed post by id
    user = CustomUser.objects.get(id=user_id)  # getting needed user by id
    send_mail(
        f'New Post: {post.title}',
        f'Post {post.title} was published.',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
