import json

from django.core.management.base import BaseCommand

from collection.extraction import BATCH_SIZE, PENDING_FILE, export_pending


class Command(BaseCommand):
    help = 'Write the next batch of listings that need extraction to data/extract/pending.json.'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=BATCH_SIZE)

    def handle(self, *args, **options):
        data = export_pending(options['limit'])
        PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
        PENDING_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        self.stdout.write(
            f"{len(data['listings'])} listings exported to {PENDING_FILE} "
            f"({data['remaining_after_this_batch']} more waiting)."
        )
