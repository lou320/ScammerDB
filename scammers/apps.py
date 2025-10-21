from django.apps import AppConfig


class ScammersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scammers'

    def ready(self):
        import scammers.signals
