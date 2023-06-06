from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView

app_name = 'blog'

urlpatterns = [
    path('', cache_page(60 * 10)(PostListView.as_view()), name='list'),  # name = blog:list
    path('<slug:slug_param>', cache_page(60 * 100)(PostDetailView.as_view()), name='detail'),  # name = blog:detail
    path('create/', PostCreateView.as_view(), name='create'),
    path('<slug:slug_param>/update/', PostUpdateView.as_view(), name='update')
]
