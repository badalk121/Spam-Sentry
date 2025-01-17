"""
Tests for the spam app.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.users.models import User
from apps.spam.models import SpamReport

class SpamReportModelTests(TestCase):
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

    def test_prevent_self_reporting(self):
        self.spam_data['phone_number'] = self.user.phone_number
        with self.assertRaises(Exception):
            SpamReport.objects.create(**self.spam_data)

class SpamAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_spam_report(self):
        url = reverse('spam-list')
        data = {
            'phone_number': '+10987654321',
            'description': 'Spam call'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_spam_likelihood(self):
        url = reverse('spam-check')
        data = {
            'phone_number': '+10987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('spam_likelihood', response.data)

    def test_get_spam_statistics(self):
        url = reverse('spam-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_reports', response.data)