from django.apps import AppConfig

class DriverMatchingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'driver_matching'

    def ready(self):
        """Import signals to ensure they are registered."""
        import driver_matching.signals
