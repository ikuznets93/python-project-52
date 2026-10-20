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


class UserPermissionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username='owner',
            password='password123',
        )
        self.other = user_model.objects.create_user(
            username='other',
            password='password123',
        )
        self.client.force_login(self.other)

    def test_anonymous_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(reverse('update', args=[self.owner.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_anonymous_cannot_delete_user(self):
        self.client.logout()

        response = self.client.post(reverse('delete', args=[self.owner.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])
        self.assertTrue(
            get_user_model().objects.filter(pk=self.owner.pk).exists()
        )

    def test_non_owner_cannot_open_update_page(self):
        response = self.client.get(reverse('update', args=[self.owner.pk]))

        self.assertRedirects(response, reverse('users'))

    def test_non_owner_cannot_update_another_user(self):
        response = self.client.post(
            reverse('update', args=[self.owner.pk]),
            {'username': 'hijacked', 'first_name': '', 'last_name': ''},
            follow=True,
        )

        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, 'Вы не можете редактировать другого пользователя'
        )
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.username, 'owner')

    def test_non_owner_cannot_delete_another_user(self):
        response = self.client.post(
            reverse('delete', args=[self.owner.pk]), follow=True
        )

        self.assertRedirects(response, reverse('users'))
        self.assertContains(
            response, 'Вы не можете удалить другого пользователя'
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.owner.pk).exists()
        )

    def test_owner_can_update_own_profile(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('update', args=[self.owner.pk]),
            {'username': 'owner', 'first_name': 'Ann', 'last_name': 'Author'},
        )

        self.assertRedirects(response, reverse('users'))
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.get_full_name(), 'Ann Author')

    def test_other_users_have_no_edit_links_in_list(self):
        response = self.client.get(reverse('users'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, reverse('update', args=[self.owner.pk])
        )
        self.assertNotContains(
            response, reverse('delete', args=[self.owner.pk])
        )


class UserCreateViewTests(TestCase):
    def test_anonymous_can_open_registration_page(self):
        response = self.client.get(reverse('create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')

    def test_user_can_register(self):
        response = self.client.post(
            reverse('create'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'john',
                'password1': 'very-secret-password-123',
                'password2': 'very-secret-password-123',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('login'))
        user = get_user_model().objects.get(username='john')
        self.assertEqual(user.get_full_name(), 'John Doe')
        self.assertTrue(user.check_password('very-secret-password-123'))
        self.assertContains(response, 'Пользователь успешно создан.')

    def test_registration_rejects_duplicate_username(self):
        get_user_model().objects.create_user(
            username='john',
            password='password123',
        )

        response = self.client.post(
            reverse('create'),
            {
                'username': 'john',
                'password1': 'very-secret-password-123',
                'password2': 'very-secret-password-123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(
            get_user_model().objects.filter(username='john').count(), 1
        )
