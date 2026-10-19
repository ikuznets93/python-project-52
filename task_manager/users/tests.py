from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


@override_settings(LANGUAGE_CODE='ru')
class UserListViewTests(TestCase):
    def test_users_list_page_displays_required_columns(self):
        user = get_user_model().objects.create_user(
            username='john',
            first_name='John',
            last_name='Doe',
            password='password123',
        )

        response = self.client.get(reverse('users'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ID')
        self.assertContains(response, 'Имя пользователя')
        self.assertContains(response, 'Полное имя')
        self.assertContains(response, 'Дата создания')
        self.assertContains(response, str(user.id))
        self.assertContains(response, user.username)
        self.assertContains(response, user.get_full_name())
        self.assertContains(response, user.date_joined.strftime('%d.%m.%Y'))


class UserDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(self.user)

    def test_user_without_tasks_is_deleted(self):
        response = self.client.post(reverse('delete', args=[self.user.pk]))

        self.assertRedirects(response, reverse('users'))
        self.assertFalse(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )

    def test_user_with_reported_task_is_not_deleted(self):
        task = Task.objects.create(
            name='Reported task',
            reporter=self.user,
            status=Status.objects.create(name='Open'),
        )

        response = self.client.post(reverse('delete', args=[self.user.pk]))

        self.assertRedirects(response, reverse('users'))
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

    def test_user_with_assigned_task_is_not_deleted(self):
        assignee = self.user
        task = Task.objects.create(
            name='Assigned task',
            reporter=get_user_model().objects.create_user(
                username='reporter',
                password='password123',
            ),
            assignee=assignee,
            status=Status.objects.create(name='Open'),
        )

        response = self.client.post(reverse('delete', args=[self.user.pk]))

        self.assertRedirects(response, reverse('users'))
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
