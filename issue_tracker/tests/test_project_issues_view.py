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
