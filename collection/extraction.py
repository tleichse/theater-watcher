import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from catalog.models import Action, Organisation
from digest.schedule import LISBON

from .models import RawListing

EXTRACT_DIR = settings.DATA_DIR / 'extract'
PENDING_FILE = EXTRACT_DIR / 'pending.json'
DRAFTS_FILE = EXTRACT_DIR / 'drafts.json'
BATCH_SIZE = 25

DRAFT_FIELDS = [
    'kind', 'pillar', 'title', 'summary', 'location', 'region', 'remote', 'age_min', 'age_max',
    'gender', 'languages', 'pay', 'fee_text', 'price_eur', 'format', 'always_open',
]
DATE_FIELDS = {
    'published_at': time(0, 0),
    'deadline_at': time(23, 59),
    'event_start': time(0, 0),
    'event_end': time(23, 59),
}


@dataclass
class ImportResult:
    created: int = 0
    duplicates: int = 0
    skipped: int = 0
    already_imported: int = 0
    errors: list = field(default_factory=list)


def export_pending(limit=BATCH_SIZE):
    listings = RawListing.objects.filter(extracted_at__isnull=True).exclude(raw_text='')
    open_actions = Action.objects.exclude(status__in=[Action.Status.REJECTED, Action.Status.EXPIRED])
    open_actions = open_actions.filter(expires_at__gt=timezone.now()) | open_actions.filter(expires_at__isnull=True)
    return {
        'today': timezone.localdate().isoformat(),
        'remaining_after_this_batch': max(listings.count() - limit, 0),
        'listings': [
            {
                'id': listing.pk,
                'source': listing.source.slug,
                'source_name': listing.source.name,
                'source_tier': listing.source.tier,
                'url': listing.url,
                'title': listing.raw_title,
                'published_at': _iso(listing.published_at),
                'fetched_at': _iso(listing.fetched_at),
                'text': listing.raw_text,
            }
            for listing in listings.select_related('source').order_by('pk')[:limit]
        ],
        'open_actions': [
            {
                'id': action.pk,
                'title': action.title,
                'organisation': action.organisation.name if action.organisation else None,
                'deadline_at': _iso(action.deadline_at),
                'source_url': action.source_url,
            }
            for action in open_actions.select_related('organisation').distinct()
        ],
    }


def import_drafts(data):
    result = ImportResult()
    for entry in data.get('results', []):
        listing = RawListing.objects.filter(pk=entry.get('listing_id')).select_related('source').first()
        if listing is None:
            result.errors.append(f"listing {entry.get('listing_id')}: not found")
            continue
        if listing.extracted_at:
            result.already_imported += 1
            continue
        try:
            with transaction.atomic():
                created, duplicates = _import_entry(listing, entry)
                listing.extracted_at = timezone.now()
                listing.skip_reason = '' if entry.get('actions') else entry['skip_reason'][:200]
                listing.save(update_fields=['extracted_at', 'skip_reason'])
        except (ValidationError, ValueError, TypeError, KeyError) as exc:
            result.errors.append(f'listing {listing.pk}: {_message(exc)}')
            continue
        if not entry.get('actions'):
            result.skipped += 1
        result.created += created
        result.duplicates += duplicates
    return result


def _import_entry(listing, entry):
    actions = entry.get('actions') or []
    if not actions and not entry.get('skip_reason'):
        raise ValueError('needs either actions or a skip_reason')
    created = duplicates = 0
    now = timezone.now()
    for draft in actions:
        duplicate = _find_duplicate(draft)
        if duplicate:
            duplicate.last_seen_at = now
            duplicate.save(update_fields=['last_seen_at'])
            duplicates += 1
            continue
        action = Action(
            source=listing.source,
            source_url=draft.get('source_url') or listing.url,
            organisation=_organisation(draft.get('organisation')),
            first_seen_at=listing.fetched_at,
            last_seen_at=now,
            status=Action.Status.PENDING_REVIEW,
            **{name: draft[name] for name in DRAFT_FIELDS if draft.get(name) is not None},
            **{name: _datetime(draft.get(name), at) for name, at in DATE_FIELDS.items()},
        )
        action.published_at = action.published_at or listing.published_at
        action.fingerprint = fingerprint(action.title, draft.get('organisation'), action.deadline_at)
        if Action.objects.filter(fingerprint=action.fingerprint).update(last_seen_at=now):
            duplicates += 1
            continue
        action.full_clean()
        action.save()
        created += 1
    return created, duplicates


def _find_duplicate(draft):
    duplicate_of = draft.get('duplicate_of')
    if duplicate_of is None:
        return None
    action = Action.objects.filter(pk=duplicate_of).first()
    if action is None:
        raise ValueError(f'duplicate_of {duplicate_of} does not exist')
    return action


def _organisation(name):
    if not name or not name.strip():
        return None
    wanted = normalise(name)
    for organisation in Organisation.objects.all():
        if normalise(organisation.name) == wanted:
            return organisation
    return Organisation.objects.create(name=name.strip())


def fingerprint(title, organisation, deadline_at):
    deadline = deadline_at.astimezone(LISBON).date().isoformat() if deadline_at else ''
    key = '|'.join([normalise(title), normalise(organisation or ''), deadline])
    return hashlib.sha256(key.encode()).hexdigest()


def normalise(text):
    text = ''.join(char for char in unicodedata.normalize('NFKD', text) if not unicodedata.combining(char))
    return ' '.join(re.sub(r'[\W_]+', ' ', text.lower()).split())


def _datetime(value, date_only_time):
    if not value:
        return None
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return datetime.combine(date.fromisoformat(value), date_only_time, LISBON)
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=LISBON)


def _iso(value):
    return value.isoformat() if value else None


def _message(exc):
    if isinstance(exc, ValidationError) and hasattr(exc, 'message_dict'):
        return '; '.join(f'{name}: {" ".join(messages)}' for name, messages in exc.message_dict.items())
    return str(exc)
