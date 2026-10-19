from django.forms import ModelForm

from task_manager.forms import StyledFormMixin
from task_manager.labels.models import Label


class LabelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Label
        fields = ['name']
