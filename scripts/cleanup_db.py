"""
Script to clean up old or invalid data from the database.
"""

import os
import django
from datetime import datetime, timedelta
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.users.models import User
from apps.contacts.models import Contact
from apps.spam.models import SpamReport

def cleanup_old_spam_reports(days=30):
    """Remove spam reports older than specified days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    SpamReport.objects.filter(created_at__lt=cutoff_date).delete()

def cleanup_duplicate_contacts():
    """Remove duplicate contacts for users."""
    for user in User.objects.all():
        seen_numbers = set()
        for contact in Contact.objects.filter(user=user):
            if contact.phone_number in seen_numbers:
                contact.delete()
            else:
                seen_numbers.add(contact.phone_number)

def cleanup_invalid_data():
    """Clean up invalid or corrupted data."""
    # Remove contacts with invalid phone numbers
    Contact.objects.filter(phone_number__regex=r'^[^+]').delete()
    
    # Remove spam reports with invalid phone numbers
    SpamReport.objects.filter(phone_number__regex=r'^[^+]').delete()

@transaction.atomic
def perform_cleanup():
    """Main function to perform database cleanup."""
    try:
        print("Cleaning up old spam reports...")
        cleanup_old_spam_reports()
        
        print("Removing duplicate contacts...")
        cleanup_duplicate_contacts()
        
        print("Cleaning up invalid data...")
        cleanup_invalid_data()
        
        print("Database cleanup completed successfully!")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    perform_cleanup()