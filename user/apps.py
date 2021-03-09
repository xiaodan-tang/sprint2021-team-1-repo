from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"

    def ready(self):    # import the signals
        import user.signals