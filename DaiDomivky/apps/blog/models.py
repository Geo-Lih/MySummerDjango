from DaiDomivky.settings import AUTH_USER_MODEL

from django.db import models
from django.urls import reverse


class Post(models.Model):
    STATUS = ((0, 'Draft'),
              (1, 'Published'))

    title = models.CharField(max_length=200, unique=True, help_text='Title for post')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(help_text='Content for post')
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.slug,))

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.author}"
