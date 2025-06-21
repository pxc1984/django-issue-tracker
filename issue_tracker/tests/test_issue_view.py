import rest_framework.test
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import *


class TestIssueViewAPI(APITestCase):
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
        cls.issue = Issue.objects.create(
            issue_id=1,
            title='it doesn`t work',
            project=cls.project,
            reporter=cls.user,
        )

        cls.url = reverse('issue view', kwargs={'project_id': cls.project.name, 'issue_id': cls.issue.issue_id})

    def setUp(self):
        self.client.force_authenticate(self.user)

    def testGetIssueSuccess(self):
        response: Response = self.client.get(self.url, {})

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, self.issue.__repr__())

    def testGetNonexistentIssue(self):
        url = reverse('issue view', kwargs={'project_id': self.project.name, 'issue_id': 9999})
        response = self.client.get(url, {})

        self.assertEqual(response.status_code, 404)

    def testGetIssueAnonymous(self):
        self.client.force_authenticate(None)

        response = self.client.get(self.url, {})

        self.assertEqual(response.status_code, 403)

    def testGetIssueUnsufficientPrivileges(self):
        self.membership.role = 0
        self.membership.save()

        response = self.client.get(self.url, {})

        self.assertEqual(response.status_code, 403)
