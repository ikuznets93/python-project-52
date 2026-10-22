from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LocalizationTests(TestCase):
    def test_russian_translation_is_active_by_default(self):
        response = self.client.get(reverse('index'))

        self.assertContains(response, 'Менеджер задач')
        self.assertNotContains(response, 'Task manager')

    def test_login_form_is_translated(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'Имя пользователя')
        self.assertContains(response, 'Пароль')

    def test_interface_has_no_untranslated_placeholders(self):
        user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(user)

        expectations = {
            reverse('users'): ('Пользователи', 'No users yet.'),
            reverse('statuses'): ('Статусы', 'No statuses yet.'),
            reverse('labels'): ('Метки', 'No labels yet.'),
            reverse('tasks'): ('Задачи', 'No tasks yet.'),
        }

        for url, (translated, untranslated) in expectations.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                body = response.content.decode()
                self.assertEqual(response.status_code, 200)
                self.assertIn(translated, body)
                self.assertNotIn(untranslated, body)

    def test_english_locale_still_available(self):
        response = self.client.get(
            reverse('index'), headers={'accept-language': 'en'}
        )

        self.assertContains(response, 'Task manager')
        self.assertNotContains(response, 'Менеджер задач')

    def test_login_page_shows_authentication_error(self):
        get_user_model().objects.create_user(
            username='john',
            password='password123',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'john', 'password': 'wrong-password'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertContains(response, 'role="alert"')
        self.assertContains(response, 'text-red-800')


class FormRenderingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.status = Status.objects.create(name='Open')
        self.client.force_login(self.user)

    def test_form_fields_have_visible_borders(self):
        response = self.client.get(reverse('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'border border-gray-300')

    def test_duplicate_name_error_is_shown_in_red(self):
        Task.objects.create(
            name='Duplicate task',
            reporter=self.user,
            status=self.status,
        )

        response = self.client.post(
            reverse('task_create'),
            {'name': 'Duplicate task', 'status': self.status.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача с таким именем уже существует')
        self.assertContains(response, 'text-red-600')


class NavigationTests(TestCase):
    def test_anonymous_sees_only_users_link(self):
        response = self.client.get(reverse('index'))
        body = response.content.decode()

        self.assertIn(f'href="{reverse("users")}"', body)
        for name in ('statuses', 'labels', 'tasks'):
            with self.subTest(name=name):
                self.assertNotIn(f'href="{reverse(name)}"', body)

    def test_authenticated_user_sees_all_app_links(self):
        user = get_user_model().objects.create_user(
            username='john',
            password='password123',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('index'))
        body = response.content.decode()

        for name in ('users', 'statuses', 'labels', 'tasks'):
            with self.subTest(name=name):
                self.assertIn(f'href="{reverse(name)}"', body)
