from django.forms import ModelForm

from task_manager.tasks.models import Task, get_default_status


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee', 'labels']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['assignee'].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )

        if self.instance.pk is None and not self.is_bound:
            default_status = get_default_status()
            if default_status is not None:
                self.initial['status'] = default_status
        