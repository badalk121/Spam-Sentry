"""
Test cases for contacts app.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.users.models import User
from .models import Contact

class ContactModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.contact_data = {
            'user': self.user,
            'name': 'Test Contact',
            'phone_number': '+10987654321'
        }

    def test_create_contact(self):
        contact = Contact.objects.create(**self.contact_data)
        self.assertEqual(contact.name, self.contact_data['name'])
        self.assertEqual(contact.phone_number, self.contact_data['phone_number'])

class ContactAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_contact_list(self):
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contact_create(self):
        url = reverse('contact-list')
        data = {
            'name': 'New Contact',
            'phone_number': '+10987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)