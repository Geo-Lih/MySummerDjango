from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignUpView, UserLoginView


app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog:list'), name='logout')
]
