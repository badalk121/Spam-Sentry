"""
Test cases for spam app.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.users.models import User
from .models import SpamReport

class SpamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.spam_data = {
            'reporter': self.user,
            'phone_number': '+10987654321',
            'description': 'Spam call'
        }

    def test_create_spam_report(self):
        report = SpamReport.objects.create(**self.spam_data)
        self.assertEqual(report.phone_number, self.spam_data['phone_number'])
        self.assertEqual(report.description, self.spam_data['description'])

class SpamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_spam_report_create(self):
        url = reverse('spam-list')
        data = {
            'phone_number': '+10987654321',
            'description': 'Spam call'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)