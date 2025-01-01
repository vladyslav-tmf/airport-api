from django.apps import AppConfig


class AirportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "airport"

    def ready(self) -> None:
        """
        Import signals when app is ready.
        Connects signal handlers for cache invalidation.
        """
        import airport.signals  # noqa
