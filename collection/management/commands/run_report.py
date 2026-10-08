from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from collection.report import latest_run, write_report


class Command(BaseCommand):
    help = 'Rewrite the report of the last collect, adding what extraction made of it.'

    def add_arguments(self, parser):
        parser.add_argument('run', nargs='?', help='A *-collect.json file in data/digests/reports (default: the latest).')

    def handle(self, *args, **options):
        run = Path(options['run']) if options['run'] else latest_run()
        if run is None:
            raise CommandError('No collect has been recorded yet. Run collect first.')
        self.stdout.write(f'Report: {write_report(run)}')
