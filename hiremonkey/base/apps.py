from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "base"

    def ready(self):
        import base.signals


# class UserConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "base"

#     def ready(self):
#         import users.signals
