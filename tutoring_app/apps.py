from django.apps import AppConfig


class TutoringAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutoring_app"
    
    def ready(self):
        import tutoring_app.models
