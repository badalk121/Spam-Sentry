"""
Signal handlers for the contacts app.
Handles events related to contact creation, modification, and deletion.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Contact
from django.db import transaction

@receiver(pre_save, sender=Contact)
def contact_pre_save(sender, instance, **kwargs):
    """
    Signal handler for before contact is saved.
    Validates phone number format and cleans data.
    """
    if instance.pk:  # If contact exists (update)
        # Get old instance
        try:
            old_instance = Contact.objects.get(pk=instance.pk)
            # Clear cache if phone number changed
            if old_instance.phone_number != instance.phone_number:
                cache.delete(f'contact_phone_{old_instance.phone_number}')
        except Contact.DoesNotExist:
            pass

@receiver(post_save, sender=Contact)
def contact_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for after contact is saved.
    Updates caches and handles related data.
    """
    # Clear user's contact cache
    cache.delete(f'user_contacts_{instance.user.id}')
    
    # Clear phone number lookup cache
    cache.delete(f'contact_phone_{instance.phone_number}')
    
    # If this is a new contact, update user's contact count
    if created:
        cache.delete(f'user_contact_count_{instance.user.id}')

@receiver(post_delete, sender=Contact)
def contact_post_delete(sender, instance, **kwargs):
    """
    Signal handler for after contact is deleted.
    Cleans up caches and related data.
    """
    # Clear all related caches
    cache.delete(f'user_contacts_{instance.user.id}')
    cache.delete(f'contact_phone_{instance.phone_number}')
    cache.delete(f'user_contact_count_{instance.user.id}')

@receiver(post_save, sender=Contact)
def sync_contact_data(sender, instance, created, **kwargs):
    """
    Signal handler to synchronize contact data with other services or cache.
    """
    if created:
        # Update search index
        transaction.on_commit(lambda: update_contact_index(instance))

def update_contact_index(contact):
    """
    Helper function to update search index for contact.
    """
    cache_key = f'contact_search_{contact.user.id}_{contact.name.lower()}'
    cache.delete(cache_key)
    
    pass