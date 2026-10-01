from django.core.management.base import BaseCommand

from catalog.models import Source
from collection.collect import collect_source, prune_raw_text
from collection.http import Fetcher


class Command(BaseCommand):
    help = 'Fetch new listings from every active source.'

    def add_arguments(self, parser):
        parser.add_argument('--source', action='append', help='Only this source slug (repeatable).')

    def handle(self, *args, **options):
        sources = Source.objects.filter(active=True)
        if options['source']:
            sources = sources.filter(slug__in=options['source'])
        fetcher = Fetcher()
        failed = 0
        for source in sources:
            result = collect_source(source, fetcher)
            if result.error:
                failed += 1
                self.stdout.write(self.style.ERROR(f'{source.slug}: {result.error}'))
            else:
                self.stdout.write(f'{source.slug}: {result.new} new, {result.updated} updated')
        self.stdout.write(f'Raw text cleared on {prune_raw_text()} listings older than 60 days.')
        if failed:
            self.stdout.write(self.style.WARNING(f'{failed} source(s) failed.'))
