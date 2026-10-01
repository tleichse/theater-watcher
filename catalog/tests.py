from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Action, Source

T0 = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)


class ExpiresAtTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name='Coffeepaste', url='https://www.coffeepaste.com/', tier='B', method='html'
        )

    def make(self, **fields):
        return Action.objects.create(
            kind='casting', pillar='theatre', title='Audição', region='centre',
            source=self.source, source_url='https://example.org/1', first_seen_at=T0, **fields
        )

    def test_deadline_wins(self):
        deadline = T0 + timedelta(days=5)
        action = self.make(deadline_at=deadline, event_start=T0 + timedelta(days=9))
        self.assertEqual(action.expires_at, deadline)

    def test_event_start_without_deadline(self):
        start = T0 + timedelta(days=9)
        self.assertEqual(self.make(event_start=start).expires_at, start)

    def test_thirty_days_after_publication(self):
        published = T0 - timedelta(days=2)
        action = self.make(published_at=published)
        self.assertEqual(action.expires_at, published + timedelta(days=30))

    def test_thirty_days_after_first_seen(self):
        self.assertEqual(self.make().expires_at, T0 + timedelta(days=30))

    def test_always_open_never_expires(self):
        self.assertIsNone(self.make(always_open=True).expires_at)

    def test_override_wins(self):
        override = T0 + timedelta(days=60)
        action = self.make(deadline_at=T0 + timedelta(days=5), expires_at_override=override)
        self.assertEqual(action.expires_at, override)

    def test_recomputed_on_partial_save(self):
        action = self.make()
        action.deadline_at = T0 + timedelta(days=3)
        action.save(update_fields=['deadline_at'])
        action.refresh_from_db()
        self.assertEqual(action.expires_at, T0 + timedelta(days=3))


class ActionAdminTests(TestCase):
    def test_changelist_renders_with_review_filter(self):
        User.objects.create_superuser('admin', 'admin@example.org', 'pw')
        self.client.login(username='admin', password='pw')
        response = self.client.get('/admin/catalog/action/', {'misses_next_issue': 'yes'})
        self.assertContains(response, 'falha a próxima edição')
