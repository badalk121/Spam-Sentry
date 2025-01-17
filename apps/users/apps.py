"""
Users app configuration.
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Users Management'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import apps.users.signals