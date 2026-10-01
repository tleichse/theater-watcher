from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from digest.gmail import authorize


class Command(BaseCommand):
    help = 'Open the browser to let theater-watcher send email from your Gmail account (one-time).'

    def handle(self, *args, **options):
        if not settings.GMAIL_CLIENT_FILE.exists():
            raise CommandError(
                f'Missing {settings.GMAIL_CLIENT_FILE}. Download the OAuth client file from Google Cloud '
                'and save it there (HOWTO.md, one-time setup, step 3).'
            )
        self.stdout.write('A browser window will open: pick your Gmail account and allow sending.')
        authorize(settings.GMAIL_CLIENT_FILE, settings.GMAIL_TOKEN_FILE)
        self.stdout.write(f'Authorised. Token saved to {settings.GMAIL_TOKEN_FILE}.')
