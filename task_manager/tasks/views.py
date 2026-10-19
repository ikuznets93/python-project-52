from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


# Create your views here.
class TaskListView(LoginRequiredMixin, FilterView):
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.select_related(
            'status', 'reporter', 'assignee'
        ).order_by('created_at')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        
        if not form.instance.status_id:
            default_status = Task.objects.filter(status__is_default=True).first()
            if default_status:
                form.instance.status = default_status.status

        return super().form_valid(form)

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