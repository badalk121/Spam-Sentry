"""
Test file for the contacts app.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.users.models import User
from apps.contacts.models import Contact

class ContactModelTests(TestCase):
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

class ContactAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='+11234567890',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_contact(self):
        url = reverse('contact-list')
        data = {
            'name': 'Test Contact',
            'phone_number': '+10987654321'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bulk_create_contacts(self):
        url = reverse('contact-bulk-create')
        data = {
            'contacts': [
                {
                    'name': 'Contact 1',
                    'phone_number': '+10987654321'
                },
                {
                    'name': 'Contact 2',
                    'phone_number': '+10987654322'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)