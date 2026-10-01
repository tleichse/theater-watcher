from dataclasses import dataclass
from datetime import timedelta

from django.utils import timezone

from catalog.models import Organisation, Source

from .adapters import ADAPTERS
from .models import RawListing
from .sources import BY_SLUG, SOURCES, load_companies

RAW_TEXT_RETENTION = timedelta(days=60)
ACTIVE_YEARS = 2


@dataclass
class Result:
    source: str
    new: int = 0
    updated: int = 0
    error: str = ''


def sync_sources():
    for entry in SOURCES:
        Source.objects.update_or_create(
            slug=entry['slug'],
            defaults={
                **{field: entry[field] for field in ('name', 'url', 'tier', 'method')},
                'active': entry.get('active', True),
            },
        )
    oldest_active = timezone.now().year - ACTIVE_YEARS
    for company in load_companies():
        validated = int(company['last_active'] or 0) >= oldest_active
        Organisation.objects.update_or_create(
            name=company['name'],
            defaults={'website': company['website'], 'validated': validated},
        )
    return len(SOURCES)


def collect_source(source, fetcher):
    result = Result(source.slug)
    entry = BY_SLUG.get(source.slug)
    if entry is None:
        result.error = 'not in collection/sources.py'
        return result
    existing = {listing.url: listing for listing in RawListing.objects.filter(source=source)}
    try:
        for listing in ADAPTERS[entry['adapter']](fetcher, entry['config'], set(existing)):
            current = existing.get(listing.url)
            if current is None:
                existing[listing.url] = RawListing.objects.create(
                    source=source,
                    url=listing.url,
                    raw_title=listing.title[:500],
                    raw_text=listing.text,
                    published_at=listing.published_at,
                )
                result.new += 1
            elif current.raw_text and current.raw_text != listing.text:
                current.raw_title = listing.title[:500]
                current.raw_text = listing.text
                current.fetched_at = timezone.now()
                current.extracted_at = None
                current.save()
                result.updated += 1
    except Exception as exc:
        result.error = f'{type(exc).__name__}: {exc}'
    return result


def prune_raw_text(now=None):
    cutoff = (now or timezone.now()) - RAW_TEXT_RETENTION
    return RawListing.objects.filter(fetched_at__lt=cutoff).exclude(raw_text='').update(raw_text='')
