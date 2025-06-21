from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import Project


class TestProjectsViewAPI(APITestCase):
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
            created_by=cls.user,
        )

        cls.url = reverse('projects view')

    def setUp(self):
        self.client.force_authenticate(self.user)

    def testGetProjectsSuccessful(self):
        # noinspection PyTypeChecker
        response: Response = self.client.get(self.url, None)
        self.assertIn('data', response.data, '"data" key not found in response.')
        self.assertEqual(len(response.data['data']), 1, 'Server returned different amount of projects.')
        self.assertEqual(response.status_code, 200, 'Server returned different status code.')
        self.assertEqual(type(response.data['data'][0]), dict, 'server didn\'t return correct type.')
        self.assertDictEqual(response.data['data'][0], self.project.__repr__())

    def testCreateProjectSuccessful(self):
        project_data = {
            'name': 'New project',
            'description': 'test description',
        }
        # noinspection PyTypeChecker
        response: Response = self.client.post(self.url, project_data)
        self.assertEqual(response.data['message'], 'created')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(name=project_data['name']).exists())

    def testCreateProjectNoName(self):
        project_data = {
            'description': 'test description',
        }
        # noinspection PyTypeChecker
        response: Response = self.client.post(self.url, project_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.all().count(), 1)

    def testCreateProjectNoDescription(self):
        project_data = {
            'name': 'New project',
        }
        # noinspection PyTypeChecker
        response: Response = self.client.post(self.url, project_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(name=project_data['name']).exists())
