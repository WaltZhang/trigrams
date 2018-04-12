from django.apps import AppConfig
from django.db.models.signals import post_save

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from django.contrib.auth.models import User
        from .signals import create_profile
        post_save.connect(create_profile, sender=User)
