from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [

    path('', PostListView.as_view(), name='list'),  # name = blog:list
    path('<slug:slug_param>', PostDetailView.as_view(), name='detail'),  # name = blog:detail
]
