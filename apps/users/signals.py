"""
Signal handlers for the users app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

@receiver(post_save, sender=User)
def clear_user_cache(sender, instance, **kwargs):
    """
    Clear user-related cache when a user is saved.
    """
    cache.delete(f'user_{instance.id}')
    cache.delete(f'user_profile_{instance.id}')