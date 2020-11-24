from django.apps import AppConfig
from django.core.management import call_command


class AtlassoAppConfig(AppConfig):
    name = "atlasso"

    def ready(self):
        # migrate in-memory db
        call_command('migrate', verbosity=1, interactive=False)