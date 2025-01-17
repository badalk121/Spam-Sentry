"""
Spam app configuration.
"""

from django.apps import AppConfig

class SpamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.spam'
    verbose_name = 'Spam Management'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import apps.spam.signals  # Import signals if you have any