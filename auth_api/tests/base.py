from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    def setUp(self):
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }
