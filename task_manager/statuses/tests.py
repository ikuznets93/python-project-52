from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(self.user)
        self.status = Status.objects.create(name='Open')

    def test_status_without_tasks_is_deleted(self):
        response = self.client.post(
            reverse('delete_status', args=[self.status.pk])
        )

        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_with_tasks_is_not_deleted(self):
        task = Task.objects.create(
            name='Task in status',
            reporter=self.user,
            status=self.status,
        )

        response = self.client.post(
            reverse('delete_status', args=[self.status.pk])
        )

        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
