from DaiDomivky.mixins import SuccessUrlMixin

from django.contrib.auth.views import LoginView
from django.views import generic

from .forms import CustomUserCreationForm, EmailAuthenticationForm


class SignUpView(SuccessUrlMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url_name = 'user:login'

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     Cart.objects.create(user=self.object)
    #
    #     return response


class UserLoginView(SuccessUrlMixin, LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'registration/login.html'
    success_url_name = 'blog:list'
