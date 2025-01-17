"""
Script to generate test data for development and testing.
"""

import os
import django
import random
from faker import Faker
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.users.models import User
from apps.contacts.models import Contact
from apps.spam.models import SpamReport

fake = Faker()

def generate_test_scenarios():
    """Generate specific test scenarios."""
    # Create a user with many contacts
    user_many_contacts = User.objects.create_user(
        username='many_contacts_user',
        phone_number='+11234567890',
        password='testpass123'
    )
    
    # Create 100 contacts for this user
    for i in range(100):
        Contact.objects.create(
            user=user_many_contacts,
            name=f'Test Contact {i}',
            phone_number=f'+1{fake.msisdn()[3:]}'
        )
    
    # Create a heavily reported spam number
    spam_number = '+19876543210'
    for _ in range(20):
        user = User.objects.create_user(
            username=fake.user_name(),
            phone_number=f'+1{fake.msisdn()[3:]}',
            password='testpass123'
        )
        SpamReport.objects.create(
            reporter=user,
            phone_number=spam_number,
            description='Test spam number'
        )

@transaction.atomic
def generate_test_data():
    """Main function to generate test data."""
    try:
        print("Generating test scenarios...")
        generate_test_scenarios()
        print("Test data generation completed successfully!")
        
    except Exception as e:
        print(f"Error generating test data: {e}")

if __name__ == '__main__':
    generate_test_data()