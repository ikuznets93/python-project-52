from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label



class LabelListView(LoginRequiredMixin, ListView):
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Label.objects.only('id', 'name', 'created_at').order_by(
            'created_at'
        )


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully removed')
    
    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(request, _('Cannot delete label'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)