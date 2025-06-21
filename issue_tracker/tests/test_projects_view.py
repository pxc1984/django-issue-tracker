from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import Project, ProjectMembership, ProjectPermission, ProjectSerializer
from issue_tracker.tests.base import BaseAPITestCase


class TestProjectsViewAPI(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.url = reverse('projects view')

    def testGetProjectsSuccessful(self):
        response: Response = self.client.get(self.url, None, format='json')
        self.assertIn('data', response.data, '"data" key not found in response.')
        self.assertEqual(len(response.data['data']), 1, 'Server returned different amount of projects.')
        self.assertEqual(response.status_code, 200, 'Server returned different status code.')
        self.assertDictEqual(response.data['data'][0], ProjectSerializer(self.project).data)

    def testGetProjectsInsufficientPermissions(self):
        new_project = Project.objects.create( name='new project' )
        ProjectMembership.objects.create(user=self.user, project=new_project, role=0) # He doesn't have any permissions in this project

        response = self.client.get(self.url, None, format='json')
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.status_code, 200)

    def testCreateProjectSuccessful(self):
        project_data = {
            'name': 'New project',
            'description': 'test description',
        }
        response: Response = self.client.post(self.url, project_data, format='json')
        self.assertEqual(response.status_code, 201)
        project = Project.objects.filter(name=project_data['name']).first()
        self.assertIsNotNone(project)
        membership = ProjectMembership.objects.filter(user=self.user, project=project).first()
        self.assertIsNotNone(membership)
        self.assertEqual(membership.role, ProjectPermission.Manage | ProjectPermission.Write | ProjectPermission.Read)

    def testCreateProjectNoName(self):
        project_data = {
            'description': 'test description',
        }
        response: Response = self.client.post(self.url, project_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.all().count(), 1)

    def testCreateProjectNoDescription(self):
        project_data = {
            'name': 'New project',
        }
        response: Response = self.client.post(self.url, project_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(name=project_data['name']).exists())

    def testCreateProjectAnonymous(self):
        self.client.force_authenticate(None)
        project_data = {
            'name': 'New project',
            'description': 'test description',
        }
        response: Response = self.client.post(self.url, project_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(name=project_data['name']).exists())

    def testCreateProjectExisting(self):
        response: Response = self.client.post(self.url, {'name': self.project.name}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.all().count(), 1)

    def testDeleteProjectSuccessful(self):
        response: Response = self.client.delete(self.url, {'name': self.project.name}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.all().count(), 0)

    def testDeleteProjectAnonymous(self):
        self.client.force_authenticate(None)
        response: Response = self.client.delete(self.url, {'name': self.project.name}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.all().count(), 1)

    def testDeleteProjectNoName(self):
        response: Response = self.client.delete(self.url, {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.all().count(), 1)

    def testDeleteProjectUnexistent(self):
        response: Response = self.client.delete(self.url, {'name': 'This project does not exist'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.all().count(), 1)

    def testDeleteProjectUnsufficientPermissions(self):
        new_data = {
            'name': 'New project',
        }
        new_project = Project.objects.create(name=new_data['name'])
        ProjectMembership.objects.create(
            user=self.user,
            project=new_project,
            role=1, # read-only access
        )

        response: Response = self.client.delete(self.url, new_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.all().count(), 2)


