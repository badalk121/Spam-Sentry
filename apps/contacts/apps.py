"""
Contacts app configuration.
"""

from django.apps import AppConfig

class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
    verbose_name = 'Contacts Management'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import apps.contacts.signals 