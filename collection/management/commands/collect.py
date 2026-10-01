from django.core.management.base import BaseCommand

from catalog.models import Source
from collection.collect import collect_source, prune_raw_text, sync_sources
from collection.http import Fetcher


class Command(BaseCommand):
    help = 'Fetch new listings from every active source.'

    def add_arguments(self, parser):
        parser.add_argument('--source', action='append', help='Only this source slug (repeatable).')

    def handle(self, *args, **options):
        self.stdout.write(f'{sync_sources()} sources synced.')
        sources = Source.objects.filter(active=True)
        if options['source']:
            sources = sources.filter(slug__in=options['source'])
        fetcher = Fetcher()
        failed = 0
        blocked = []
        for source in sources:
            result = collect_source(source, fetcher)
            if result.blocked:
                blocked.append(source.slug)
            elif result.error:
                failed += 1
                self.stdout.write(self.style.ERROR(f'{source.slug}: {result.error}'))
            else:
                self.stdout.write(f'{source.slug}: {result.new} new, {result.updated} updated')
        self.stdout.write(f'Raw text cleared on {prune_raw_text()} listings older than 60 days.')
        if blocked:
            self.stdout.write(
                f"{len(blocked)} site(s) blocked by the work network's filter, not a site problem "
                f"(collect from another network to get them): {', '.join(blocked)}"
            )
        if failed:
            self.stdout.write(self.style.WARNING(f'{failed} source(s) failed.'))
