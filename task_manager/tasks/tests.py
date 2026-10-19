from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskFilterTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(
            username='author',
            first_name='Ann',
            last_name='Author',
            password='password123',
        )
        self.assignee = user_model.objects.create_user(
            username='assignee',
            first_name='Sam',
            last_name='Assignee',
            password='password123',
        )
        self.other = user_model.objects.create_user(
            username='other',
            password='password123',
        )

        self.open_status = Status.objects.create(name='Open')
        self.done_status = Status.objects.create(name='Done')
        self.bug_label = Label.objects.create(name='bug')
        self.feature_label = Label.objects.create(name='feature')

        self.own_open_bug = Task.objects.create(
            name='Own open bug',
            reporter=self.author,
            assignee=self.assignee,
            status=self.open_status,
        )
        self.own_open_bug.labels.add(self.bug_label)

        self.own_done = Task.objects.create(
            name='Own done task',
            reporter=self.author,
            assignee=self.other,
            status=self.done_status,
        )
        self.own_done.labels.add(self.feature_label)

        self.foreign_open = Task.objects.create(
            name='Foreign open task',
            reporter=self.other,
            assignee=self.assignee,
            status=self.open_status,
        )
        self.foreign_open.labels.add(self.bug_label)

        self.client.login(username='author', password='password123')
        self.url = reverse('tasks')

    def test_filter_form_is_shown(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="status"')
        self.assertContains(response, 'name="executor"')
        self.assertContains(response, 'name="label"')
        self.assertContains(response, 'name="self_tasks"')

    def test_filter_by_status(self):
        response = self.client.get(self.url, {'status': self.open_status.pk})

        self.assertContains(response, self.own_open_bug.name)
        self.assertContains(response, self.foreign_open.name)
        self.assertNotContains(response, self.own_done.name)

    def test_filter_by_assignee(self):
        response = self.client.get(self.url, {'executor': self.assignee.pk})

        self.assertContains(response, self.own_open_bug.name)
        self.assertContains(response, self.foreign_open.name)
        self.assertNotContains(response, self.own_done.name)

    def test_filter_by_label(self):
        response = self.client.get(self.url, {'label': self.bug_label.pk})

        self.assertContains(response, self.own_open_bug.name)
        self.assertContains(response, self.foreign_open.name)
        self.assertNotContains(response, self.own_done.name)

    def test_filter_own_tasks(self):
        response = self.client.get(self.url, {'self_tasks': 'on'})

        self.assertContains(response, self.own_open_bug.name)
        self.assertContains(response, self.own_done.name)
        self.assertNotContains(response, self.foreign_open.name)

    def test_combined_filters(self):
        response = self.client.get(
            self.url,
            {
                'status': self.open_status.pk,
                'executor': self.assignee.pk,
                'label': self.bug_label.pk,
                'self_tasks': 'on',
            },
        )

        self.assertContains(response, self.own_open_bug.name)
        self.assertNotContains(response, self.own_done.name)
        self.assertNotContains(response, self.foreign_open.name)


class TaskDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='author',
            first_name='Ann',
            last_name='Author',
            password='password123',
        )
        self.status = Status.objects.create(name='Open')
        self.client.login(username='author', password='password123')

    def test_detail_page_renders_task_without_assignee(self):
        task = Task.objects.create(
            name='Task without assignee',
            reporter=self.user,
            status=self.status,
            assignee=None,
        )

        response = self.client.get(reverse('task_detail', args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)
        self.assertContains(response, 'Task without assignee')

    def test_detail_page_renders_task_with_assignee(self):
        task = Task.objects.create(
            name='Task with assignee',
            reporter=self.user,
            assignee=self.user,
            status=self.status,
        )

        response = self.client.get(reverse('task_detail', args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.get_full_name())


class TaskPermissionTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(
            username='author',
            password='password123',
        )
        self.other = user_model.objects.create_user(
            username='other',
            password='password123',
        )
        self.status = Status.objects.create(name='Open')
        self.task = Task.objects.create(
            name='Shared task',
            reporter=self.author,
            status=self.status,
        )

    def test_anonymous_cannot_delete_task(self):
        response = self.client.post(
            reverse('task_delete', args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_non_author_cannot_delete_task(self):
        self.client.force_login(self.other)

        response = self.client.post(
            reverse('task_delete', args=[self.task.pk]), follow=True
        )

        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.assertContains(response, 'Только автор может удалить эту задачу.')

    def test_author_can_delete_task(self):
        self.client.force_login(self.author)

        response = self.client.post(reverse('task_delete', args=[self.task.pk]))

        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_authenticated_user_can_edit_foreign_task(self):
        self.client.force_login(self.other)

        response = self.client.post(
            reverse('task_update', args=[self.task.pk]),
            {'name': 'Renamed by other', 'status': self.status.pk},
        )

        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Renamed by other')

    def test_delete_link_is_hidden_from_non_author(self):
        self.client.force_login(self.other)

        response = self.client.get(reverse('tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, reverse('task_delete', args=[self.task.pk])
        )

    def test_delete_link_is_visible_to_author(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse('tasks'))

        self.assertContains(
            response, reverse('task_delete', args=[self.task.pk])
        )


class TaskFormDefaultStatusTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='author',
            password='password123',
        )

    def test_default_status_is_preselected(self):
        status = Status.objects.create(name='New', is_default=True)

        form = TaskForm()

        self.assertEqual(form.initial['status'], status.pk)

    def test_nothing_is_preselected_without_a_default_status(self):
        Status.objects.update(is_default=False)

        form = TaskForm()

        self.assertIsNone(form.initial.get('status'))

    def test_existing_task_keeps_its_own_status(self):
        open_status = Status.objects.create(name='Open')
        Status.objects.create(name='New', is_default=True)
        task = Task.objects.create(
            name='Task',
            reporter=self.user,
            status=open_status,
        )

        form = TaskForm(instance=task)

        self.assertEqual(form.initial['status'], open_status.pk)

    def test_create_page_renders_preselected_default_status(self):
        status = Status.objects.create(name='New', is_default=True)
        self.client.force_login(self.user)

        response = self.client.get(reverse('task_create'))

        self.assertContains(response, f'value="{status.pk}" selected')
