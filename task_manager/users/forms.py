from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

INPUT_CLASS = (
    'mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 '
    'text-sm text-gray-900 shadow-sm focus:border-blue-500 '
    'focus:outline-none focus:ring-1 focus:ring-blue-500'
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'autofocus': True}),
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
    )