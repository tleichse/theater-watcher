import io
import shutil
import tempfile
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from unittest import mock

import base64

from google.auth.exceptions import RefreshError

from django.core import mail
from django.core.management import CommandError, call_command
from django.test import SimpleTestCase, TestCase, override_settings

from catalog.models import Action, Organisation, Source

from .gmail import SEND_URL, GmailApiBackend, GmailAuthRequired, load_credentials
from .models import Digest, DigestItem
from .render import deadline_chip, facts, render
from .schedule import LISBON, current_issue_at, misses_next_issue, next_send_at
from .selection import Section, select


def lisbon(*args):
    return datetime(*args, tzinfo=LISBON)


SEND_AT = lisbon(2026, 10, 5, 9)


class NextSendAtTests(SimpleTestCase):
    def test_midweek_goes_to_next_monday(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 1, 15)), lisbon(2026, 10, 5, 9))

    def test_monday_before_send_time_is_same_day(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 5, 8)), lisbon(2026, 10, 5, 9))

    def test_monday_after_send_time_is_next_week(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 5, 9)), lisbon(2026, 10, 12, 9))

    def test_across_dst_change(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 24, 12)), lisbon(2026, 10, 26, 9))


class CurrentIssueAtTests(SimpleTestCase):
    def test_monday_after_the_slot_still_belongs_to_that_issue(self):
        self.assertEqual(current_issue_at(lisbon(2026, 10, 5, 10, 30)), SEND_AT)
        self.assertEqual(current_issue_at(lisbon(2026, 10, 6, 8)), SEND_AT)

    def test_later_in_the_week_points_to_next_monday(self):
        self.assertEqual(current_issue_at(lisbon(2026, 10, 7, 12)), lisbon(2026, 10, 12, 9))


class MissesNextIssueTests(SimpleTestCase):
    now = lisbon(2026, 10, 1, 15)

    def test_closing_within_margin_misses(self):
        self.assertTrue(misses_next_issue(lisbon(2026, 10, 6, 9), self.now))

    def test_closing_after_margin_is_kept(self):
        self.assertFalse(misses_next_issue(lisbon(2026, 10, 6, 9) + timedelta(minutes=1), self.now))

    def test_never_expiring_is_kept(self):
        self.assertFalse(misses_next_issue(None, self.now))


class DigestDataMixin:
    def setUp(self):
        self.source = Source.objects.create(
            slug='coffeepaste', name='Coffeepaste', url='https://www.coffeepaste.com/', tier='B', method='html'
        )
        self.organisation = Organisation.objects.create(name='Teatro Exemplo')

    def make(self, status='approved', days=20, **fields):
        fields.setdefault('deadline_at', SEND_AT + timedelta(days=days))
        return Action.objects.create(
            kind=fields.pop('kind', 'casting'), pillar=fields.pop('pillar', 'theatre'),
            title=fields.pop('title', 'Audição'), region='centre', source=self.source,
            source_url='https://example.org/1', organisation=self.organisation, status=status,
            first_seen_at=SEND_AT - timedelta(days=3), **fields,
        )

    def sections_of(self, action):
        selection = select(SEND_AT)
        return [section for section, items in selection.sections.items() if any(i.action == action for i in items)]


class SelectionTests(DigestDataMixin, TestCase):
    def test_only_approved_actions_are_eligible(self):
        self.make(status='pending_review')
        self.make(status='rejected')
        self.assertEqual(select(SEND_AT).total, 0)

    def test_needs_more_than_24_hours_left(self):
        closing = self.make(deadline_at=SEND_AT + timedelta(hours=24))
        still_open = self.make(deadline_at=SEND_AT + timedelta(hours=25))
        self.assertEqual(self.sections_of(closing), [])
        self.assertEqual(self.sections_of(still_open), [Section.CLOSING_SOON])

    def test_closing_within_a_week_moves_to_ultimos_dias_only(self):
        self.assertEqual(self.sections_of(self.make(days=7)), [Section.CLOSING_SOON])
        self.assertEqual(self.sections_of(self.make(days=8)), [Section.THEATRE])

    def test_sections_by_kind_and_pillar(self):
        self.assertEqual(self.sections_of(self.make(pillar='dubbing')), [Section.DUBBING])
        self.assertEqual(self.sections_of(self.make(kind='training', pillar='cinema')), [Section.TRAINING])
        self.assertEqual(self.sections_of(self.make(kind='grant')), [Section.GRANTS])
        self.assertEqual(self.sections_of(self.make(kind='signal', days=3)), [Section.RADAR])
        always_open = self.make(always_open=True, deadline_at=None)
        self.assertEqual(self.sections_of(always_open), [Section.ALWAYS_OPEN])

    def test_new_until_shared_in_an_earlier_issue(self):
        shared = self.make(title='Já enviada')
        self.make(title='Nova', days=30)
        earlier = Digest.objects.create(number=1, scheduled_for=SEND_AT - timedelta(days=7), subject='#1')
        DigestItem.objects.create(digest=earlier, action=shared, section='theatre', position=0)
        items = select(SEND_AT).sections[Section.THEATRE]
        self.assertEqual([(item.action.title, item.is_new) for item in items], [('Nova', True), ('Já enviada', False)])

    def test_order_within_a_group_is_by_expiry(self):
        later = self.make(title='Mais tarde', days=30)
        sooner = self.make(title='Mais cedo', days=10)
        items = select(SEND_AT).sections[Section.THEATRE]
        self.assertEqual([item.action for item in items], [sooner, later])


class FormattingTests(DigestDataMixin, TestCase):
    def test_deadline_chip(self):
        self.assertEqual(deadline_chip(self.make(days=1), SEND_AT), 'Fecha amanhã')
        self.assertEqual(deadline_chip(self.make(days=3), SEND_AT), 'Fecha em 3 dias')
        self.assertEqual(deadline_chip(self.make(days=10), SEND_AT), 'Candidaturas até 15 out')
        starts = self.make(deadline_at=None, event_start=lisbon(2026, 10, 16))
        self.assertEqual(deadline_chip(starts, SEND_AT), 'Começa a 16 out')
        self.assertEqual(deadline_chip(self.make(always_open=True, deadline_at=None), SEND_AT), '')

    def test_facts(self):
        casting = self.make(location='Lisboa', fee_text='1 300 €', age_min=18, age_max=35)
        self.assertEqual(facts(casting), 'Lisboa · 1 300 € · 18–35 anos')
        training = self.make(kind='training', location='Porto', price_eur=Decimal('90.00'))
        self.assertEqual(facts(training), 'Porto · 90 €')
        free = self.make(kind='training', remote=True, price_eur=Decimal('0'))
        self.assertEqual(facts(free), 'À distância · Gratuito')


class RenderTests(DigestDataMixin, TestCase):
    def test_every_pillar_section_appears_and_css_is_inlined(self):
        self.make(title='Audição para nova peça')
        rendered = render(select(SEND_AT))
        self.assertEqual(rendered.number, 1)
        self.assertEqual(rendered.subject, 'relATOR #1 · 1 nova ação')
        for label in ['Teatro', 'Cinema', 'Televisão', 'Publicidade', 'Dobragem']:
            self.assertIn(label, rendered.html)
            self.assertIn(label.upper(), rendered.text)
        self.assertEqual(rendered.html.count('Sem novidades esta semana'), 4)
        self.assertIn('Audição para nova peça', rendered.text)
        self.assertNotIn('<style', rendered.html)
        self.assertIn('style="', rendered.html)

    def test_pillar_tag_only_outside_pillar_sections(self):
        self.make(title='Audição para nova peça', pillar='theatre')
        self.make(title='Workshop de câmara', kind='training', pillar='cinema')
        rendered = render(select(SEND_AT))
        self.assertNotIn('>Teatro</span>', rendered.html)
        self.assertIn('>Cinema</span>', rendered.html)
        self.assertNotIn('  Teatro · ', rendered.text)
        self.assertIn('  Cinema · ', rendered.text)

    def test_empty_optional_sections_are_left_out(self):
        rendered = render(select(SEND_AT))
        self.assertNotIn('Formação', rendered.html)
        self.assertNotIn('No radar', rendered.html)

    def test_build_digest_writes_files_and_records_nothing(self):
        self.make()
        output = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, output)
        with mock.patch('digest.render.OUTPUT_DIR', output):
            call_command('build_digest', at='2026-10-05T09:00', stdout=io.StringIO())
        self.assertEqual(sorted(path.name for path in output.iterdir()), ['issue-1-2026-10-05.html', 'issue-1-2026-10-05.txt'])
        self.assertEqual(Digest.objects.count(), 0)


@override_settings(GMAIL_ADDRESS='sender@example.org', DIGEST_RECIPIENTS=['reader@example.org', 'friend@example.org'])
class SendDigestTests(DigestDataMixin, TestCase):
    def send(self, *args):
        output = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, output)
        out = io.StringIO()
        with mock.patch('digest.render.OUTPUT_DIR', output):
            call_command('send_digest', '--at', '2026-10-05T09:00', *args, stdout=out)
        return out.getvalue()

    def test_sends_html_and_text_then_records_the_issue(self):
        shared = self.make(title='Audição para nova peça')
        closing = self.make(title='Fecha já', days=3)
        self.send()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ['sender@example.org'])
        self.assertEqual(message.bcc, ['reader@example.org', 'friend@example.org'])
        self.assertEqual(message.subject, 'relATOR #1 · 2 novas ações, 1 a fechar')
        self.assertIn('Audição para nova peça', message.body)
        self.assertIn('Audição para nova peça', message.alternatives[0].content)
        self.assertIn('cid:logo', message.alternatives[0].content)
        logo = next(part for part in message.message().walk() if part.get_content_type() == 'image/png')
        self.assertEqual(logo['Content-ID'], '<logo>')
        digest = Digest.objects.get()
        self.assertEqual((digest.number, digest.scheduled_for), (1, SEND_AT))
        recorded = {(item.action, item.section, item.was_new) for item in digest.items.all()}
        self.assertEqual(recorded, {(shared, 'theatre', True), (closing, 'closing_soon', True)})
        next_week = select(SEND_AT + timedelta(days=7)).sections[Section.THEATRE]
        self.assertEqual([(item.action, item.is_new) for item in next_week], [(shared, False)])

    def test_refuses_to_send_the_same_issue_twice(self):
        self.make()
        self.send()
        with self.assertRaisesMessage(CommandError, 'already sent'):
            self.send()
        self.assertEqual(len(mail.outbox), 1)

    def test_resend_sends_the_same_issue_again_without_recording_it(self):
        self.make()
        self.send()
        out = self.send('--resend')
        self.assertEqual([message.subject for message in mail.outbox], ['relATOR #1 · 1 nova ação'] * 2)
        self.assertEqual(mail.outbox[1].bcc, ['reader@example.org', 'friend@example.org'])
        self.assertEqual(Digest.objects.count(), 1)
        self.assertIn('not recorded again', out)

    def test_preview_of_a_sent_issue_keeps_its_number(self):
        self.make()
        self.send()
        self.assertEqual(render(select(SEND_AT)).number, 1)

    def test_resend_needs_an_issue_that_was_sent(self):
        self.make()
        with self.assertRaisesMessage(CommandError, 'without --resend'):
            self.send('--resend')
        self.assertEqual(len(mail.outbox), 0)

    def test_test_send_records_nothing(self):
        self.make()
        self.send('--test')
        self.assertTrue(mail.outbox[0].subject.startswith('[TESTE] '))
        self.assertEqual((mail.outbox[0].to, mail.outbox[0].bcc), (['sender@example.org'], []))
        self.assertEqual(Digest.objects.count(), 0)

    def test_failed_send_records_nothing(self):
        self.make()
        with mock.patch('digest.send.EmailMultiAlternatives.send', side_effect=ConnectionResetError(10054, 'reset')):
            with self.assertRaisesMessage(CommandError, 'Gmail did not accept the email'):
                self.send()
        self.assertEqual(Digest.objects.count(), 0)

    def test_expired_authorisation_asks_to_authorise_again(self):
        self.make()
        error = GmailAuthRequired('The Gmail authorisation expired or was revoked.')
        with mock.patch('digest.send.EmailMultiAlternatives.send', side_effect=error):
            with self.assertRaisesMessage(CommandError, 'authorize_gmail'):
                self.send()
        self.assertEqual(Digest.objects.count(), 0)

    def test_refuses_when_nothing_is_approved(self):
        self.make(status='pending_review')
        with self.assertRaisesMessage(CommandError, 'Nothing to send'):
            self.send()

    @override_settings(GMAIL_ADDRESS='')
    def test_refuses_without_gmail_settings(self):
        self.make()
        with self.assertRaisesMessage(CommandError, 'GMAIL_ADDRESS'):
            self.send()
        self.assertEqual(len(mail.outbox), 0)


class GmailBackendTests(SimpleTestCase):
    def test_posts_the_encoded_message_to_the_gmail_api(self):
        from django.core.mail import EmailMultiAlternatives

        message = EmailMultiAlternatives('Assunto ção', 'texto', 'from@example.org', ['to@example.org'], bcc=['a@example.org', 'b@example.org'])
        message.attach_alternative('<p>html</p>', 'text/html')
        session = mock.Mock()
        with mock.patch('digest.gmail.load_credentials'), mock.patch('digest.gmail.AuthorizedSession', return_value=session):
            sent = GmailApiBackend(token_file='token.json').send_messages([message])
        self.assertEqual(sent, 1)
        url, = session.post.call_args.args
        raw = base64.urlsafe_b64decode(session.post.call_args.kwargs['json']['raw'])
        self.assertEqual(url, SEND_URL)
        self.assertIn(b'to@example.org', raw)
        self.assertIn(b'Bcc: a@example.org, b@example.org', raw)
        self.assertIn(b'text/html', raw)
        session.post.return_value.raise_for_status.assert_called_once()

    def test_missing_token_needs_authorisation(self):
        with self.assertRaisesMessage(GmailAuthRequired, 'not been authorised'):
            load_credentials(Path(tempfile.gettempdir()) / 'no-such-gmail-token.json')

    def test_failed_refresh_needs_authorisation(self):
        token = Path(tempfile.mkdtemp()) / 'token.json'
        self.addCleanup(shutil.rmtree, token.parent)
        token.write_text('{}', encoding='utf-8')
        credentials = mock.Mock(valid=False)
        credentials.refresh.side_effect = RefreshError('invalid_grant: Token has been expired or revoked.')
        with mock.patch('digest.gmail.Credentials.from_authorized_user_file', return_value=credentials):
            with self.assertRaisesMessage(GmailAuthRequired, 'expired or was revoked'):
                load_credentials(token)
