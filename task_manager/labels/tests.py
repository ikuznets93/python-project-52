from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LabelListViewTests(TestCase):
    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('labels'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_sees_labels(self):
        user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(user)
        label = Label.objects.create(name='bug')

        response = self.client.get(reverse('labels'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, label.name)


class LabelCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('label_create'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_can_create_label(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('label_create'),
            {'name': 'bug'},
            follow=True,
        )

        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='bug').exists())
        self.assertContains(response, 'Метка успешно создана')

    def test_duplicate_label_name_is_rejected(self):
        self.client.force_login(self.user)
        Label.objects.create(name='bug')

        response = self.client.post(
            reverse('label_create'),
            {'name': 'bug'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        self.assertEqual(Label.objects.filter(name='bug').count(), 1)


class LabelUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.label = Label.objects.create(name='bug')
        self.client.force_login(self.user)

    def test_anonymous_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(
            reverse('label_update', args=[self.label.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_can_update_label(self):
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'feature'},
            follow=True,
        )

        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'feature')
        self.assertContains(response, 'Метка успешно изменена')


class LabelDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.label = Label.objects.create(name='bug')
        self.client.force_login(self.user)

    def test_anonymous_cannot_delete_label(self):
        self.client.logout()

        response = self.client.post(
            reverse('label_delete', args=[self.label.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_without_tasks_is_deleted(self):
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assertContains(response, 'Метка успешно удалена')

    def test_label_with_tasks_is_not_deleted(self):
        task = Task.objects.create(
            name='Task with label',
            reporter=self.user,
            status=Status.objects.create(name='Open'),
        )
        task.labels.add(self.label)

        response = self.client.post(
            reverse('label_delete', args=[self.label.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        self.assertContains(response, 'Невозможно удалить метку')
