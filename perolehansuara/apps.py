from django.apps import AppConfig


class PerolehansuaraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "perolehansuara"

    def ready(self):
        import perolehansuara.signals
