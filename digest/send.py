from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from .models import Digest, DigestItem
from .render import render
from .selection import select

GMAIL_CLIP_BYTES = 100_000


class CannotSend(Exception):
    pass


def send_issue(send_at, test=False):
    if not settings.GMAIL_ADDRESS or not settings.DIGEST_RECIPIENT:
        raise CannotSend('Set GMAIL_ADDRESS, GMAIL_APP_PASSWORD and DIGEST_RECIPIENT in .env (see HOWTO.md).')
    if not test and Digest.objects.filter(scheduled_for=send_at).exists():
        raise CannotSend(f'The issue for {send_at:%Y-%m-%d %H:%M} was already sent.')
    selection = select(send_at)
    if not selection.total:
        raise CannotSend('Nothing to send: no approved action is open for this issue.')
    rendered = render(selection)
    subject = f'[TESTE] {rendered.subject}' if test else rendered.subject
    message = EmailMultiAlternatives(subject, rendered.text, to=[settings.DIGEST_RECIPIENT])
    message.attach_alternative(rendered.html, 'text/html')
    message.send()
    if not test:
        _record(rendered, selection)
    return rendered, selection


@transaction.atomic
def _record(rendered, selection):
    digest = Digest.objects.create(
        number=rendered.number,
        scheduled_for=selection.send_at,
        sent_at=timezone.now(),
        subject=rendered.subject,
    )
    DigestItem.objects.bulk_create(
        DigestItem(digest=digest, action=item.action, section=section, position=position, was_new=item.is_new)
        for section, items in selection.sections.items()
        for position, item in enumerate(items)
    )
