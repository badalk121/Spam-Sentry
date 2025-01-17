"""
Test cases for users app.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'phone_number': '+11234567890',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])

    def test_phone_number_validation(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['phone_number'] = '1234'  # Invalid format
        with self.assertRaises(Exception):
            User.objects.create_user(**invalid_user_data)

class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'phone_number': '+10987654321',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)