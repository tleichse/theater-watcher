import json

from django.core.management.base import BaseCommand

from collection.extraction import DRAFTS_FILE, import_drafts


class Command(BaseCommand):
    help = 'Import draft actions from data/extract/drafts.json as pending review.'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='?', default=str(DRAFTS_FILE))

    def handle(self, *args, **options):
        with open(options['path'], encoding='utf-8') as handle:
            result = import_drafts(json.load(handle))
        self.stdout.write(
            f'{result.created} created, {result.duplicates} duplicates, {result.skipped} skipped, '
            f'{result.already_imported} already imported, {len(result.errors)} errors.'
        )
        for error in result.errors:
            self.stdout.write(self.style.ERROR(error))
