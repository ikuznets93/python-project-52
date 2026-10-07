from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return (
            Task.objects.select_related('status', 'reporter', 'assignee')
            .only(
                'name',
                'created_at',
                'status__name',
                'reporter__first_name',
                'reporter__last_name',
                'assignee__first_name',
                'assignee__last_name',
            )
            .order_by('created_at')
        )

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class CreateTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')

class TaskDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')

    def test_func(self):
        task = self.get_object()
        return task.reporter == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, _('Only the author can delete this task.'))
        return redirect('tasks')