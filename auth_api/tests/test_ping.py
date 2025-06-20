from django.urls import reverse
from rest_framework import status

from auth_api.tests.base import BaseTestCase


class PingAPITest(BaseTestCase):
    def test_ping_endpoint(self):
        url = reverse('ping')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'pong'})
