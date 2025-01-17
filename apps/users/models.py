"""
User-related models.
Contains User model and related functionality.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds phone number and additional fields.
    """
    
    # Phone number validation regex
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )

    # Additional fields
    phone_number = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=17,
        unique=True,
        db_index=True,
        help_text=_('Required. Unique phone number for the user.')
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        null=True,
        help_text=_('Optional. User\'s email address.')
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Designates whether this user has verified their phone number.')
    )

    # Meta configuration
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.username} ({self.phone_number})"

    def get_full_name(self):
        """
        Returns the user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Returns the user's short name.
        """
        return self.first_name

    def clean(self):
        """
        Custom validation for user model.
        """
        super().clean()
        if self.email:
            self.email = self.email.lower()