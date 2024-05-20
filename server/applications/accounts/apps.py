from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.accounts'
    
    def ready(self) -> None:
        import applications.accounts.signals
