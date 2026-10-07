from django.forms import ModelForm
from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['assignee'].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )
        