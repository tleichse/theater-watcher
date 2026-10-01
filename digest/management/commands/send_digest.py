from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from digest.render import write
from digest.schedule import LISBON, current_issue_at
from digest.send import GMAIL_CLIP_BYTES, CannotSend, send_issue


class Command(BaseCommand):
    help = 'Send the current issue to DIGEST_RECIPIENT through Gmail and record what was shared.'

    def add_arguments(self, parser):
        parser.add_argument('--at', help='Send time in Lisbon, e.g. 2026-10-05T09:00 (default: the current issue, Monday 09:00).')
        parser.add_argument('--test', action='store_true', help='Send with a [TESTE] subject and record nothing.')

    def handle(self, *args, **options):
        send_at = datetime.fromisoformat(options['at']).replace(tzinfo=LISBON) if options['at'] else current_issue_at()
        try:
            rendered, selection = send_issue(send_at, test=options['test'])
        except CannotSend as error:
            raise CommandError(str(error))
        html_path, _ = write(rendered, send_at)
        self.stdout.write(f'Sent "{rendered.subject}" to {settings.DIGEST_RECIPIENT}: {selection.total} items.')
        self.stdout.write('Test send: nothing recorded.' if options['test'] else f'Recorded as issue #{rendered.number}. Copy kept at {html_path}')
        if len(rendered.html.encode()) > GMAIL_CLIP_BYTES:
            self.stdout.write(self.style.WARNING('The HTML is over 100 KB, so Gmail will clip it ("Mensagem cortada").'))
