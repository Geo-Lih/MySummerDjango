from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, EmailAuthenticationForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):  # overwriting of success_url attr does not work(
        return reverse_lazy('user:login')


class UserLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('blog:list')
