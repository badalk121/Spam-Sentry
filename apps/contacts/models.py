"""
Models for the contacts app.
"""

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    """
    Model for storing user contacts.
    """
    
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text=_('User who owns this contact')
    )
    name = models.CharField(
        max_length=100,
        help_text=_('Contact name')
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text=_('Contact phone number')
    )
    email = models.EmailField(
        null=True,
        blank=True,
        help_text=_('Contact email address (optional)')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        unique_together = ('user', 'phone_number')
        ordering = ['name']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def clean(self):
        """
        Custom validation for contact model.
        """
        super().clean()
        if self.email:
            self.email = self.email.lower()