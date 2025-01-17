"""
Tests for the users app.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from apps.contacts.models import Contact

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'phone_number': '+11234567890',
            'password': 'testpass123'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_phone_number_validation(self):
        self.user_data['phone_number'] = 'invalid'
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)

class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'phone_number': '+10987654321',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_search(self):
        url = reverse('user-search')
        response = self.client.get(url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        url = reverse('user-profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)