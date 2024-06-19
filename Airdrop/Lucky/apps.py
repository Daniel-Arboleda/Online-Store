# Lucky/apps.py

from django.apps import AppConfig

class LuckyConfig(AppConfig):
    name = 'Lucky'

    def ready(self):
        import Lucky.signals  # Asegúrate de que esto apunta al módulo correcto
