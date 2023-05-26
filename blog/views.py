from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    context_object_name = 'list'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_url_kwarg = 'slug_param'
    context_object_name = 'post'
