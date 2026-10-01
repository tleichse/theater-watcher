from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from digest.gmail import GmailAuthRequired
from digest.render import write
from digest.schedule import LISBON, current_issue_at
from digest.send import GMAIL_CLIP_BYTES, CannotSend, send_issue


class Command(BaseCommand):
    help = 'Send the current issue to DIGEST_RECIPIENTS (in Bcc) through Gmail and record what was shared.'

    def add_arguments(self, parser):
        parser.add_argument('--at', help='Send time in Lisbon, e.g. 2026-10-05T09:00 (default: the current issue, Monday 09:00).')
        parser.add_argument('--test', action='store_true', help='Send with a [TESTE] subject and record nothing.')

    def handle(self, *args, **options):
        send_at = datetime.fromisoformat(options['at']).replace(tzinfo=LISBON) if options['at'] else current_issue_at()
        try:
            rendered, selection = send_issue(send_at, test=options['test'])
        except CannotSend as error:
            raise CommandError(str(error))
        except GmailAuthRequired as error:
            raise CommandError(f'{error} Run: uv run python manage.py authorize_gmail. Nothing was recorded.')
        except OSError as error:
            raise CommandError(f'Gmail did not accept the email ({error}). Nothing was recorded.')
        html_path, _ = write(rendered, send_at)
        if options['test']:
            self.stdout.write(f'Sent "{rendered.subject}" to {settings.GMAIL_ADDRESS} only: {selection.total} items.')
        else:
            readers = len(settings.DIGEST_RECIPIENTS)
            self.stdout.write(f'Sent "{rendered.subject}" to {readers} reader(s) in Bcc: {selection.total} items.')
        self.stdout.write('Test send: nothing recorded.' if options['test'] else f'Recorded as issue #{rendered.number}. Copy kept at {html_path}')
        if len(rendered.html.encode()) > GMAIL_CLIP_BYTES:
            self.stdout.write(self.style.WARNING('The HTML is over 100 KB, so Gmail will clip it ("Mensagem cortada").'))
