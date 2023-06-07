from DaiDomivky.constants import StatusType
from DaiDomivky.mixins import PermissionHandlerMixin, SlugifyMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView


from .models import Post


class PostListView(ListView):
    """
    View for displaying a list of blog posts.
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'list'
    paginate_by = 4

    def get_queryset(self):
        """
        Returns the queryset of blog posts.
        - Retrieves the origin queryset and fetches related 'author' objects with .select_related('author').
        - Filters the posts based on the user's authentication status and post status.
        - Returns the filtered queryset.
        """
        post_qs = super().get_queryset().select_related('author')

        if self.request.user.is_authenticated:
            # Retrieve all published posts or unpublished posts authored by the current user
            post_qs = post_qs.filter(
                Q(status=StatusType.PUBLISHED) | Q(author=self.request.user, status=StatusType.DRAFT))
        else:
            post_qs = post_qs.filter(status=StatusType.PUBLISHED)

        return post_qs


class PostDetailView(DetailView):
    """
    View for displaying a single blog post in detail.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    slug_url_kwarg = 'slug_param'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """
        Retrieves the blog post object.
        """
        post_obj = super().get_object()
        if post_obj.status == StatusType.DRAFT and self.request.user != post_obj.author:
            raise Http404("Post not found.")
        return post_obj

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PostCreateView(PermissionHandlerMixin, SlugifyMixin, LoginRequiredMixin, CreateView):
    """
    View for creating a new blog post.
    """
    model = Post
    template_name = 'blog/post_create.html'
    fields = ['title', 'content', 'status']

    def get_success_url(self):
        """
        Returns the URL to redirect to upon successful post creation.
        """
        return reverse_lazy('blog:list')


class PostUpdateView(PermissionHandlerMixin, SlugifyMixin, LoginRequiredMixin, UpdateView):
    """
    View for updating an existing blog post.
    """
    model = Post
    template_name = 'blog/post_update.html'
    slug_url_kwarg = 'slug_param'
    fields = ['title', 'content', 'status']

    def get_success_url(self):
        """
        Returns the URL to redirect to upon successful post update.
        """
        return self.object.get_absolute_url()
