from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

LISBON = ZoneInfo('Europe/Lisbon')
SEND_WEEKDAY = 0
SEND_TIME = time(9, 0)
ELIGIBILITY_MARGIN = timedelta(hours=24)


def next_send_at(now=None):
    now = (now or timezone.now()).astimezone(LISBON)
    days_ahead = (SEND_WEEKDAY - now.weekday()) % 7
    candidate = datetime.combine(now.date() + timedelta(days=days_ahead), SEND_TIME, LISBON)
    if candidate <= now:
        candidate = datetime.combine(candidate.date() + timedelta(days=7), SEND_TIME, LISBON)
    return candidate


def misses_next_issue(expires_at, now=None):
    if expires_at is None:
        return False
    return expires_at <= next_send_at(now) + ELIGIBILITY_MARGIN
