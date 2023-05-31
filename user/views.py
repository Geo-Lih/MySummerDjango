from django.contrib.auth.views import LoginView
from DaiDomivky.mixins import SuccessUrlMixin
from django.views import generic

from .forms import CustomUserCreationForm, EmailAuthenticationForm


class SignUpView(SuccessUrlMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url_name = 'user:login'


class UserLoginView(SuccessUrlMixin, LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'registration/login.html'
    success_url_name = 'blog:list'
