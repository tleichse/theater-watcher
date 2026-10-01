from django.core.management.base import BaseCommand

from collection.collect import sync_sources


class Command(BaseCommand):
    help = 'Create or update every source listed in collection/sources.py.'

    def handle(self, *args, **options):
        self.stdout.write(f'{sync_sources()} sources synced.')
