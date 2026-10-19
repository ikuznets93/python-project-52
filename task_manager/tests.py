from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
        response = self.client.get(reverse('index'), headers={'accept-language': 'en'})

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
