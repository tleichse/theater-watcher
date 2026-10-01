from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from .models import Digest, DigestItem
from .render import LOGO, LOGO_CID, render
from .selection import select

GMAIL_CLIP_BYTES = 100_000


class CannotSend(Exception):
    pass


class DigestEmail(EmailMultiAlternatives):
    def message(self, **kwargs):
        # Django 6.1 has no API for inline images, so the logo is attached as a "related" part of
        # the HTML body, which is what the template's cid: link points to.
        msg = super().message(**kwargs)
        msg.get_body(('html',)).add_related(LOGO.read_bytes(), 'image', 'png', cid=f'<{LOGO_CID}>')
        return msg


def send_issue(send_at, test=False, resend=False):
    if not settings.GMAIL_ADDRESS or not settings.DIGEST_RECIPIENTS:
        raise CannotSend('Set GMAIL_ADDRESS and DIGEST_RECIPIENTS in .env (see HOWTO.md).')
    sent = Digest.objects.filter(scheduled_for=send_at).first()
    if resend and sent is None:
        raise CannotSend(f'The issue for {send_at:%Y-%m-%d %H:%M} has not been sent yet. Send it without --resend.')
    if sent and not test and not resend:
        raise CannotSend(
            f'The issue for {send_at:%Y-%m-%d %H:%M} was already sent. '
            'To send it again, add --resend (it keeps its number and is not recorded twice).'
        )
    selection = select(send_at)
    if not selection.total:
        raise CannotSend('Nothing to send: no approved action is open for this issue.')
    rendered = render(selection)
    subject = f'[TESTE] {rendered.subject}' if test else rendered.subject
    # Readers go in Bcc so nobody sees the others' addresses; a test copy only goes to the sender.
    bcc = [] if test else settings.DIGEST_RECIPIENTS
    message = DigestEmail(subject, rendered.text, to=[settings.GMAIL_ADDRESS], bcc=bcc)
    message.attach_alternative(rendered.html, 'text/html')
    message.send()
    if not test and not resend:
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
