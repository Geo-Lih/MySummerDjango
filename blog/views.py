from DaiDomivky.constants import StatusType
from DaiDomivky.mixins import SlugifyMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Post


class PostListView(ListView):
    model = Post
    # queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    context_object_name = 'list'

    def get_queryset(self):
        post_qs = super().get_queryset()  # get origin queryset
        if self.request.user.is_authenticated:
            # Retrieve all published posts or unpublished posts authored by the current user
            post_qs = post_qs.filter(
                Q(status=StatusType.PUBLISHED) | Q(author=self.request.user, status=StatusType.DRAFT))
        else:
            post_qs = post_qs.filter(status=StatusType.PUBLISHED)
        return post_qs


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_url_kwarg = 'slug_param'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post_obj = super().get_object()
        if post_obj.status == StatusType.DRAFT and self.request.user != post_obj.author:
            raise Http404("Post not found.")
        return post_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PostCreateView(SlugifyMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content', 'status']  # form fields

    # contex_object_name = form by default

    def get_success_url(self):
        return reverse_lazy('blog:list')


class PostUpdateView(SlugifyMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    slug_url_kwarg = 'slug_param'
    fields = ['title', 'content', 'status']

    def get_success_url(self):
        return self.object.get_absolute_url()
