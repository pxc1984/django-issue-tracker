import rest_framework
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import ProjectMembership
from issue_tracker.tests.base import BaseAPITestCase


class TestProjectMembersViewAPI(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="Owner",
            password='passwd123',
        )
        super().setUpTestData()

    def setUp(self):
        super().setUp()
        self.url = reverse('project members view', kwargs={'project_id': self.project.name})

    def testListMembersSuccess(self):
        response: Response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['username'], self.user.username)
        self.assertEqual(response.data['data'][0]['roles'], 'Read|Write|Manage')

    def testAnonymousAccess(self):
        self.client.force_authenticate(None)

        response: Response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, 403)

    def testUnexistentProject(self):
        url = reverse('project members view', kwargs={'project_id': 'qwery'})

        response: Response = self.client.get(url, {})
        self.assertEqual(response.status_code, 400)

    def testNotEnoughPermissions(self):
        self.client.force_authenticate(self.user1)

        response: Response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, 403)

        response: Response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 403)

    def testEditMemberPermissionsSuccess(self):
        ProjectMembership.objects.create(
            user=self.user,
            project=self.project,
            role=3,
        )

        self.testAddMemberPermissionsSuccess()

    def testAddMemberPermissionsSuccess(self):
        data = {
            'username': self.user1,
            'role': 1,
        }

        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        membership = ProjectMembership.objects.filter(
            user=self.user,
            project=self.project,
            role=1,
        ).first()
        self.assertIsNotNone(membership)

    def testDeleteMemberPermissionsSuccess(self):
        data = {
            'username': self.user,
            'role': 0,
        }

        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        membership = ProjectMembership.objects.filter(
            user=self.user,
            project=self.project,
        ).first()
        self.assertEqual(membership.role, 0)

    def testEditMemberPermissionsInvalidUsername(self):
        data = {
            'role': 1,
        }

        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)

    def testEditMemberPermissionsNonexistentUser(self):
        data = {
            'username': 'invalid',
            'role': 1,
        }

        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)

    def testEditMemberPermissionsNoRole(self):
        data = {
            'username': self.user,
        }

        response: Response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)


