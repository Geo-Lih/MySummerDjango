from django.http import Http404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView

from .models import Post


class PostListView(ListView):
    model = Post
    # queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(status=1) | queryset.filter(author=self.request.user, status=0)
        else:
            queryset = queryset.filter(status=1)
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_url_kwarg = 'slug_param'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_authenticated or self.request.user != self.object.author:
            raise Http404("Post not found.")
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content', 'status']

    def get_success_url(self):
        return reverse_lazy('blog:list')

    def form_valid(self, form):  # creating slug for post
        post = form.save(commit=False)
        post.author = self.request.user
        post.slug = slugify(post.title)
        post.save()
        return super().form_valid(form)
