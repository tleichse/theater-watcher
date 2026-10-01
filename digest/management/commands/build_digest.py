from datetime import datetime

from django.core.management.base import BaseCommand

from digest.render import render, write
from digest.schedule import LISBON, next_send_at
from digest.selection import select


class Command(BaseCommand):
    help = 'Render the next issue to data/digests/ (HTML and plain text) without sending it.'

    def add_arguments(self, parser):
        parser.add_argument('--at', help='Send time in Lisbon, e.g. 2026-10-05T09:00 (default: next Monday 09:00).')

    def handle(self, *args, **options):
        send_at = datetime.fromisoformat(options['at']).replace(tzinfo=LISBON) if options['at'] else next_send_at()
        selection = select(send_at)
        rendered = render(selection)
        html_path, text_path = write(rendered, send_at)
        self.stdout.write(rendered.subject)
        self.stdout.write(f'{selection.total} items. Preview: {html_path}')
        self.stdout.write(f'Text: {text_path}')
