from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.forms import CustomUserCreationForm

# Create your views here.
class UserListView(ListView):
    template_name = 'users/index.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return (
            get_user_model()
            .objects.exclude(is_superuser=True)
            .only('username', 'first_name', 'last_name', 'date_joined')
        ).order_by('date_joined')


class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = _("User created successfully.")


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    fields = ['first_name', 'last_name', 'username']
    success_url = reverse_lazy('users')
    success_message = _("User updated successfully.")
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _("User deleted successfully.")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.reported_tasks.exists() or user.assigned_tasks.exists():
            messages.error(request, _('Cannot delete user'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)