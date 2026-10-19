from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

SELECT_CLASS = (
    'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 '
    'text-sm text-gray-900 shadow-sm focus:border-blue-500 '
    'focus:outline-none focus:ring-1 focus:ring-blue-500'
)
CHECKBOX_CLASS = 'h-4 w-4 rounded border-gray-300 text-blue-600'


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    executor = ModelChoiceFilter(
        field_name='assignee',
        queryset=get_user_model().objects.all(),
        label=_('Assignee'),
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    label = ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label=_('Label'),
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    self_tasks = BooleanFilter(
        method='filter_self_tasks',
        label=_('Only my tasks'),
        widget=forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].field.label_from_instance = lambda user: (
            user.get_full_name() or user.username
        )

    def filter_self_tasks(self, queryset, name, value):
        if value is True and getattr(self, 'request', None):
            return queryset.filter(reporter=self.request.user)
        return queryset
