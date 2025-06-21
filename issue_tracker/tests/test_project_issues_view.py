from django.urls import reverse

from issue_tracker.models import *
from issue_tracker.tests.base import BaseAPITestCase


class TestProjectIssuesViewAPI(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.issue = Issue.objects.create(
            issue_id=1,
            title='it doesn`t work',
            project=cls.project,
            reporter=cls.user,
        )

        cls.url = reverse('project issues view', kwargs={'project_id': cls.project.name})

    def test_anonymous_access(self):
        self.client.force_authenticate(None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_get_project_issues_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_project_issues_no_access(self):
        self.client.force_authenticate(self.user1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
