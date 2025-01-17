"""
Script to populate the database with sample data.
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

def create_users(num_users=50):
    """Create sample users."""
    users = []
    for _ in range(num_users):
        try:
            user = User.objects.create_user(
                username=fake.user_name(),
                phone_number=f'+1{fake.msisdn()[3:]}',
                email=fake.email(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            users.append(user)
        except Exception as e:
            print(f"Error creating user: {e}")
    return users

def create_contacts(users, contacts_per_user=10):
    """Create sample contacts for users."""
    for user in users:
        for _ in range(random.randint(5, contacts_per_user)):
            try:
                Contact.objects.create(
                    user=user,
                    name=fake.name(),
                    phone_number=f'+1{fake.msisdn()[3:]}',
                    email=fake.email() if random.random() > 0.5 else None
                )
            except Exception as e:
                print(f"Error creating contact: {e}")

def create_spam_reports(users, reports_per_user=5):
    """Create sample spam reports."""
    phone_numbers = [f'+1{fake.msisdn()[3:]}' for _ in range(20)]
    
    for user in users:
        for _ in range(random.randint(0, reports_per_user)):
            try:
                SpamReport.objects.create(
                    reporter=user,
                    phone_number=random.choice(phone_numbers),
                    description=fake.text(max_nb_chars=100)
                )
            except Exception as e:
                print(f"Error creating spam report: {e}")

@transaction.atomic
def populate_database():
    """Main function to populate the database."""
    try:
        print("Creating users...")
        users = create_users()
        
        print("Creating contacts...")
        create_contacts(users)
        
        print("Creating spam reports...")
        create_spam_reports(users)
        
        print("Database population completed successfully!")
        
    except Exception as e:
        print(f"Error populating database: {e}")

if __name__ == '__main__':
    populate_database()