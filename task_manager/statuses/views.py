from django.shortcuts import render

from task_manager.statuses.models import Status
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class StatusListView(ListView):
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    
    def get_queryset(self):
        return Status.objects.only('id', 'name', 'created_at').order_by(
            'created_at'
        )

class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')


class UpdateStatusView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully updated')


class DeleteStatusView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')