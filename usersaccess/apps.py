from django.apps import AppConfig


class UsersAccessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersaccess'

    def ready(self):
        import usersaccess.signals



