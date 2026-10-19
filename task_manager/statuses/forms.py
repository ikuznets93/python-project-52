from django.forms import ModelForm

from task_manager.forms import StyledFormMixin
from task_manager.statuses.models import Status


class StatusForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Status
        fields = ['name']
