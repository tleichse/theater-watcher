from datetime import datetime, timedelta

from django.test import SimpleTestCase

from .schedule import LISBON, misses_next_issue, next_send_at


def lisbon(*args):
    return datetime(*args, tzinfo=LISBON)


class NextSendAtTests(SimpleTestCase):
    def test_midweek_goes_to_next_monday(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 1, 15)), lisbon(2026, 10, 5, 9))

    def test_monday_before_send_time_is_same_day(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 5, 8)), lisbon(2026, 10, 5, 9))

    def test_monday_after_send_time_is_next_week(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 5, 9)), lisbon(2026, 10, 12, 9))

    def test_across_dst_change(self):
        self.assertEqual(next_send_at(lisbon(2026, 10, 24, 12)), lisbon(2026, 10, 26, 9))


class MissesNextIssueTests(SimpleTestCase):
    now = lisbon(2026, 10, 1, 15)

    def test_closing_within_margin_misses(self):
        self.assertTrue(misses_next_issue(lisbon(2026, 10, 6, 9), self.now))

    def test_closing_after_margin_is_kept(self):
        self.assertFalse(misses_next_issue(lisbon(2026, 10, 6, 9) + timedelta(minutes=1), self.now))

    def test_never_expiring_is_kept(self):
        self.assertFalse(misses_next_issue(None, self.now))
