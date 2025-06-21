import rest_framework
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import Project, ProjectMembership, Issue, IssueStatus, IssuePriority


class TestProjectIssueCreateViewAPI(APITestCase):
    client: rest_framework.test.APIClient
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="Test user",
            password='passwd123',
        )

        # Create a test project
        cls.project = Project.objects.create(
            name='Test Project',
            description='This is project description',
        )
        cls.membership = ProjectMembership.objects.create(
            user=cls.user,
            project=cls.project,
            role=7,
        )

        cls.url = reverse('create issue', kwargs={'project_id': cls.project.name})

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_create_issue_success(self):
        data = {
            'title': 'Test Issue',
            'description': 'Test Description',
            'status': IssueStatus.OPEN.value,
            'priority': IssuePriority.LOW.value,
        }
        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Issue.objects.filter(title='Test Issue').exists())
        issue = Issue.objects.get(title='Test Issue')
        self.assertEqual(issue.description, 'Test Description')
        self.assertEqual(issue.status, IssueStatus.OPEN.value)
        self.assertEqual(issue.priority, 0)
        self.assertEqual(issue.reporter, self.user)
        self.assertEqual(issue.project, self.project)
        self.assertEqual(issue.issue_id, 1)

    def test_create_issue_without_title(self):
        data = {
            'description': 'Test Description',
            'status': str(IssueStatus.OPEN.value)
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Title is required')

    def test_create_issue_with_invalid_status(self):
        data = {
            'title': 'Test Issue',
            'description': 'Test Description',
            'status': '999'  # Invalid status
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid issue status')

    def test_create_issue_with_invalid_priority(self):
        data = {
            'title': 'Test Issue',
            'description': 'Test Description',
            'status': str(IssueStatus.OPEN.value),
            'priority': '5'  # Invalid priority
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid issue priority')

    def test_create_issue_without_description(self):
        data = {
            'title': 'Test Issue',
            'status': str(IssueStatus.OPEN.value)
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        issue = Issue.objects.get(title='Test Issue')
        self.assertEqual(issue.description, 'No description provided.')

    def test_create_issue_with_string_status(self):
        data = {
            'title': 'Test Issue',
            'description': 'Test Description',
            'status': 'OPEN'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 201)
        issue = Issue.objects.get(title='Test Issue')
        self.assertEqual(issue.status, IssueStatus.OPEN.value)

    def test_create_issue_nonexistent_project(self):
        url = reverse('create issue', kwargs={'project_id': 'nonexistent-project'})
        data = {
            'title': 'Test Issue',
            'description': 'Test Description'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 403)

    def test_create_issue_unauthorized(self):
        self.client.force_authenticate(None)
        data = {
            'title': 'Test Issue',
            'description': 'Test Description'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 403)

    def test_create_issue_insufficient_privileges(self):
        self.membership.role = 0  # No permissions
        self.membership.save()

        data = {
            'title': 'Test Issue',
            'description': 'Test Description'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 403)

    def test_create_issue_sequential_ids(self):
        # Create first issue
        data1 = {
            'title': 'First Issue',
            'description': 'First Description'
        }
        response1 = self.client.post(self.url, data1)
        self.assertEqual(response1.status_code, 201)

        # Create second issue
        data2 = {
            'title': 'Second Issue',
            'description': 'Second Description'
        }
        response2 = self.client.post(self.url, data2)
        self.assertEqual(response2.status_code, 201)

        first_issue = Issue.objects.get(title='First Issue')
        second_issue = Issue.objects.get(title='Second Issue')
        self.assertEqual(first_issue.issue_id, 1)
        self.assertEqual(second_issue.issue_id, 2)

    def test_create_issue_unexistent_project(self):
        url = reverse('create issue', kwargs={'project_id': 'invalid'})
        data = {
            'title': "My first issue",
            'description': 'First description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_create_issue_nonstring_description(self):
        data = {
            'title': "My first issue",
            'description': {'text': 'description', 'length': 4}
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
