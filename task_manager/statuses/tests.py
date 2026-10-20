from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusListViewTests(TestCase):
    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('statuses'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_sees_statuses(self):
        user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('statuses'))

        self.assertEqual(response.status_code, 200)


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

    def test_anonymous_cannot_delete_status(self):
        self.client.logout()

        response = self.client.post(
            reverse('delete_status', args=[self.status.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())


class DefaultStatusTests(TestCase):
    def test_default_status_is_created_on_deploy(self):
        status = Status.objects.get(is_default=True)

        self.assertEqual(status.name, _('New'))

    def test_new_default_status_resets_the_previous_one(self):
        first = Status.objects.create(name='First', is_default=True)
        second = Status.objects.create(name='Second', is_default=True)

        first.refresh_from_db()

        self.assertTrue(second.is_default)
        self.assertFalse(first.is_default)
        self.assertEqual(Status.objects.filter(is_default=True).count(), 1)

    def test_status_form_does_not_expose_the_default_flag(self):
        form = StatusForm()

        self.assertNotIn('is_default', form.fields)

    def test_database_rejects_two_default_statuses(self):
        first = Status.objects.create(name='First')
        second = Status.objects.create(name='Second')

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Status.objects.filter(pk__in=[first.pk, second.pk]).update(
                    is_default=True
                )


class StatusCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('create_status'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_can_create_status(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('create_status'),
            {'name': 'In progress'},
            follow=True,
        )

        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='In progress').exists())
        self.assertContains(response, 'Статус успешно создан')

    def test_duplicate_status_name_is_rejected(self):
        self.client.force_login(self.user)
        Status.objects.create(name='Open')

        response = self.client.post(
            reverse('create_status'),
            {'name': 'Open'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        self.assertEqual(Status.objects.filter(name='Open').count(), 1)


class StatusUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.status = Status.objects.create(name='Open')
        self.client.force_login(self.user)

    def test_anonymous_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(
            reverse('update_status', args=[self.status.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_can_update_status(self):
        response = self.client.post(
            reverse('update_status', args=[self.status.pk]),
            {'name': 'Done'},
            follow=True,
        )

        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Done')
        self.assertContains(response, 'Статус успешно изменён')
