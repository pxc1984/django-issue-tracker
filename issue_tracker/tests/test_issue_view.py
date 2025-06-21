from django.urls import reverse
from rest_framework.response import Response

from issue_tracker.models import *
from issue_tracker.tests.base import BaseAPITestCase


class TestIssueViewAPI(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.issue = Issue.objects.create(
            issue_id=1,
            title='it doesn`t work',
            project=cls.project,
            reporter=cls.user,
        )

        cls.url = reverse('issue view', kwargs={'project_id': cls.project.name, 'issue_id': cls.issue.issue_id})

    def testGetIssueSuccess(self):
        response: Response = self.client.get(self.url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, IssueSerializer(self.issue).data)

    def testGetNonexistentIssue(self):
        url = reverse('issue view', kwargs={'project_id': self.project.name, 'issue_id': 9999})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 404)

    def testGetIssueAnonymous(self):
        self.client.force_authenticate(None)

        response = self.client.get(self.url, {}, format='json')

        self.assertEqual(response.status_code, 403)

    def testGetIssueUnsufficientPrivileges(self):
        self.membership.role = 0
        self.membership.save()

        response = self.client.get(self.url, {}, format='json')

        self.assertEqual(response.status_code, 403)
