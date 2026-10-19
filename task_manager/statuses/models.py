from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default'),
        help_text=_('This status is preselected when a task is created'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['is_default'],
                condition=Q(is_default=True),
                name='unique_default_status',
                violation_error_message=_('Only one status can be default'),
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            with transaction.atomic():
                Status.objects.exclude(pk=self.pk).filter(
                    is_default=True
                ).update(is_default=False)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
