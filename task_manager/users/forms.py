from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.forms import StyledFormMixin


class CustomUserCreationForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']


class CustomAuthenticationForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(),
    )
