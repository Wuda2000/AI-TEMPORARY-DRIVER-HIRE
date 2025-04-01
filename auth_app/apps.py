from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'

    def ready(self):
        """Connect the post_migrate signal to create groups after migrations."""
        from .signals import create_groups
        post_migrate.connect(create_groups, sender=self)
