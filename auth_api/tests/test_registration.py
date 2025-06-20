from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from auth_api.tests.base import BaseTestCase


class RegisterAPITest(BaseTestCase):
    def test_successful_registration(self):
        url = reverse('register')
        response = self.client.post(url, self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_registration(self):
        url = reverse('register')
        invalid_data = {
            'username': 'testuser',
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password_registration(self):
        url = reverse('register')
        invalid_data = {
            "username": "testuser",
            "password": "weak",
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_username_registration(self):
        url = reverse('register')
        invalid_data = {
            'password': 'passwd',
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_exists(self):
        url = reverse('register')
        user_data = {
            "username": "createduser",
            "password": "passwd123",
            "email": "createduser@example.com",
        }
        User.objects.create_user(**user_data).save()

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User already exists.')
