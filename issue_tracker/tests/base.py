import rest_framework
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from issue_tracker.models import Project, ProjectMembership, ProjectPermission


class BaseAPITestCase(APITestCase):
    client: rest_framework.test.APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="Test user",
            password='passwd123',
        )
        cls.user1 = User.objects.create_user(
            username="Test user 1",
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
            role=ProjectPermission.Read|ProjectPermission.Write|ProjectPermission.Manage,
        )

    def setUp(self):
        self.client.force_authenticate(self.user)
