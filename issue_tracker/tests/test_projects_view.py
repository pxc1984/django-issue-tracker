from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import Project


class TestProjectsViewAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
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
        self.client.force_login(self.user)

    def testGetProjectsSuccessful(self):
        # noinspection PyTypeChecker
        response: Response = self.client.get(self.url, None)
        self.assertTrue(type(response), Response)
        self.assertIn('data', response.data, '"data" key not found in response.')
        self.assertEqual(len(response.data['data']), 1, 'Server returned different amount of projects.')
        self.assertEqual(response.status_code, 200, 'Server returned different status code.')
        self.assertEqual(type(response.data['data'][0]), dict, 'server didn\'t return correct type.')
        self.assertDictEqual(response.data['data'][0], self.project.__repr__())
