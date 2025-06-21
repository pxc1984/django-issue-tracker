from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import Project, ProjectMembership, ProjectPermission


# noinspection PyTypeChecker
class TestProjectMembersViewAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="Owner",
            password='passwd123',
        )
        cls.user = User.objects.create_user(
            username="Test user",
            password='passwd124',
        )

        # Create a test project
        cls.project = Project.objects.create(
            name='TestProject',
            description='This is project description',
        )
        ProjectMembership.objects.create(
            user=cls.owner,
            project=cls.project,
            role=7,
        )

    def setUp(self):
        self.client.force_authenticate(self.owner)

    def testListMembersSuccess(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        response: Response = self.client.get(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['username'], self.owner.username)
        self.assertEqual(response.data['data'][0]['roles'], 'Owner')

    def testAnonymousAccess(self):
        self.client.force_authenticate(None)

        url = reverse('project members view', kwargs={'project_id': self.project.name})

        response: Response = self.client.get(url, {})
        self.assertEqual(response.status_code, 403)

    def testUnexistentProject(self):
        url = reverse('project members view', kwargs={'project_id': 'qwery'})

        response: Response = self.client.get(url, {})
        self.assertEqual(response.status_code, 400)

    def testNotEnoughPermissions(self):
        self.client.force_authenticate(self.user)

        url = reverse('project members view', kwargs={'project_id': self.project.name})

        response: Response = self.client.get(url, {})
        self.assertEqual(response.status_code, 403)

        response: Response = self.client.post(url, {})
        self.assertEqual(response.status_code, 403)

    def testEditMemberPermissionsSuccess(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        ProjectMembership.objects.create(
            user=self.user,
            project=self.project,
            role=3,
        )

        data = {
            'username': self.user,
            'role': 1,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        membership = ProjectMembership.objects.filter(
            user=self.user,
            project=self.project,
            role=1,
        ).first()
        self.assertIsNotNone(membership)

    def testAddMemberPermissionsSuccess(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        data = {
            'username': self.user,
            'role': 1,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        membership = ProjectMembership.objects.filter(
            user=self.user,
            project=self.project,
            role=1,
        ).first()
        self.assertIsNotNone(membership)

    def testDeleteMemberPermissionsSuccess(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        data = {
            'username': self.user,
            'role': 0,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        membership = ProjectMembership.objects.filter(
            user=self.user,
            project=self.project,
        ).first()
        self.assertEqual(membership.role, 0)

    def testEditMemberPermissionsInvalidUsername(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        data = {
            'role': 1,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def testEditMemberPermissionsNonexistentUser(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        data = {
            'username': 'invalid',
            'role': 1,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def testEditMemberPermissionsNoRole(self):
        url = reverse('project members view', kwargs={'project_id': self.project.name})

        data = {
            'username': self.user,
        }

        response: Response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)


