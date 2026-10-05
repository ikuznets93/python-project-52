from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
