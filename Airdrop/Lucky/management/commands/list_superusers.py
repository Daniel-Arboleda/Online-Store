from django.core.management.base import BaseCommand
from Lucky.models import CustomUser




class Command(BaseCommand):
    help = 'List all superusers'

    def handle(self, *args, **kwargs):
        superusers = CustomUser.objects.filter(is_superuser=True)
        if superusers.exists():
            for user in superusers:
                self.stdout.write(self.style.SUCCESS(f'{user.email}'))
        else:
            self.stdout.write(self.style.WARNING('No superusers found'))