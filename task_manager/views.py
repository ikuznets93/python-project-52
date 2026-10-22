from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'


class LoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response


class LogoutView(auth_views.LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, _('You are logged out'))
        return response
