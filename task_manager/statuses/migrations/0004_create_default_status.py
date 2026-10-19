from django.conf import settings
from django.db import migrations
from django.utils import translation
from django.utils.translation import gettext as _


def default_status_name():
    # Migrations run with translations deactivated, so activate the project
    # language explicitly to store a localized status name.
    with translation.override(settings.LANGUAGE_CODE):
        return _('New')


def create_default_status(apps, schema_editor):
    Status = apps.get_model('statuses', 'Status')
    name = default_status_name()

    if Status.objects.filter(is_default=True).exists():
        return

    status = Status.objects.filter(name=name).first()
    if status is None:
        Status.objects.create(name=name, is_default=True)
    else:
        status.is_default = True
        status.save(update_fields=['is_default'])


def delete_default_status(apps, schema_editor):
    Status = apps.get_model('statuses', 'Status')
    Status.objects.filter(name=default_status_name(), is_default=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0003_alter_status_is_default_status_unique_default_status'),
    ]

    operations = [
        migrations.RunPython(create_default_status, delete_default_status),
    ]
