from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

#from task_manager.labels.models import Label
from task_manager.statuses.models import Status


def get_default_status():
    status = Status.objects.filter(is_default=True).first()
    return status.pk if status else None


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name'),
        error_messages={'unique': _('Task with this Name already exists')},
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reported_tasks',
        verbose_name=_('Reporter'),
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='assigned_tasks',
        verbose_name=_('Assignee'),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        default=get_default_status,
        related_name='tasks',
        verbose_name=_('Status'),
    )
    #labels = models.ManyToManyField(
     #   Label, blank=True, related_name='tasks', verbose_name=_('Labels')
    #)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name