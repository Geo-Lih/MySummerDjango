from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)  # if no fields = username by default


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email', max_length=254)  # redefining the username

    def clean(self):  # simple validation
        username = self.cleaned_data.get('username')
        if username and '@' not in username:
            raise forms.ValidationError("Enter a valid email address.")
        return super().clean()
