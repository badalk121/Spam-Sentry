"""
Models for the spam app.
"""

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class SpamReport(models.Model):
    """
    Model for storing spam reports.
    """
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='spam_reports',
        help_text=_('User who reported the spam')
    )
    phone_number = models.CharField(
        max_length=17,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in format: '+999999999'"
        )],
        help_text=_('Reported phone number')
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_('Optional description of spam activity')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('spam report')
        verbose_name_plural = _('spam reports')
        unique_together = ('reporter', 'phone_number')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Spam report by {self.reporter} for {self.phone_number}"

    def clean(self):
        """
        Validate that users cannot report their own number.
        """
        if self.reporter.phone_number == self.phone_number:
            raise models.ValidationError(
                _("You cannot report your own number as spam.")
            )