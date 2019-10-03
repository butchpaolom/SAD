from django.apps import AppConfig


class ApiProcConfig(AppConfig):
    name = 'api_proc'

    def ready(self):
        import api_proc.signals
