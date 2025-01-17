"""
Signal handlers for the spam app.
Handles events related to spam report creation and modification.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models import Count
from .models import SpamReport

@receiver(post_save, sender=SpamReport)
def spam_report_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for after spam report is saved.
    Updates spam likelihood calculations and caches.
    """
    # Clear spam likelihood cache
    cache.delete(f'spam_likelihood_{instance.phone_number}')
    
    # Clear spam statistics cache
    cache.delete('spam_statistics')
    
    if created:
        # Update report count cache
        cache.delete(f'spam_report_count_{instance.phone_number}')
        
        # Recalculate spam likelihood
        update_spam_likelihood(instance.phone_number)

@receiver(post_delete, sender=SpamReport)
def spam_report_post_delete(sender, instance, **kwargs):
    """
    Signal handler for after spam report is deleted.
    Updates caches and recalculates spam likelihood.
    """
    # Clear all related caches
    cache.delete(f'spam_likelihood_{instance.phone_number}')
    cache.delete(f'spam_report_count_{instance.phone_number}')
    cache.delete('spam_statistics')
    
    # Recalculate spam likelihood
    update_spam_likelihood(instance.phone_number)

def update_spam_likelihood(phone_number):
    """
    Helper function to update spam likelihood calculation.
    """
    # Get total reports for this number
    total_reports = SpamReport.objects.filter(
        phone_number=phone_number
    ).count()
    
    # Get unique reporters count
    unique_reporters = SpamReport.objects.filter(
        phone_number=phone_number
    ).values('reporter').distinct().count()
    
    # Calculate likelihood (example algorithm)
    likelihood = min((total_reports * 0.1) + (unique_reporters * 0.2), 1.0)
    
    # Cache the result for 1 hour
    cache.set(
        f'spam_likelihood_{phone_number}',
        likelihood,
        3600  # 1 hour
    )

@receiver(post_save, sender=SpamReport)
def update_spam_statistics(sender, instance, created, **kwargs):
    """
    Signal handler to update spam statistics.
    """
    if created:
        # Clear statistics cache
        cache.delete('spam_statistics')
        
        # Update top spammers list
        update_top_spammers()

def update_top_spammers():
    """
    Helper function to update top spammers list.
    """
    top_spammers = SpamReport.objects.values(
        'phone_number'
    ).annotate(
        report_count=Count('id')
    ).order_by('-report_count')[:10]
    
    # Cache the result for 1 hour
    cache.set('top_spammers', list(top_spammers), 3600)