import json
from collections import Counter
from dataclasses import asdict
from datetime import datetime

from django.conf import settings
from django.db.models import Count

from catalog.models import Action, Source

from .models import RawListing

REPORT_DIR = settings.DATA_DIR / 'digests' / 'reports'
GROUPS = {
    'co-': 'Theatre companies (companies.csv)',
    'pr-': 'Producers, casting, dubbing, funders (producers.csv)',
    've-': 'Venues and festivals (venues.csv)',
    'sc-': 'Schools (schools.csv)',
}
NAMED = 'Named sources (sources.py)'


def save_run(results, started_at, finished_at, filtered, last_action_id):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{started_at.astimezone():%Y-%m-%d-%H%M}-collect.json"
    path.write_text(json.dumps({
        'started_at': started_at.isoformat(),
        'finished_at': finished_at.isoformat(),
        'filtered': filtered,
        # Actions above this id were created after the run started, whatever listing they came from.
        'last_action_id': last_action_id,
        'results': [asdict(result) for result in results],
    }, ensure_ascii=False, indent=1), encoding='utf-8')
    return path


def latest_run():
    runs = sorted(REPORT_DIR.glob('*-collect.json'))
    return runs[-1] if runs else None


def write_report(run_path):
    run = json.loads(run_path.read_text(encoding='utf-8'))
    path = run_path.with_name(run_path.name.replace('-collect.json', '-report.md'))
    path.write_text(render(run), encoding='utf-8')
    return path


def render(run):
    started = datetime.fromisoformat(run['started_at'])
    finished = datetime.fromisoformat(run['finished_at'])
    results = run['results']
    active = list(Source.objects.filter(active=True).annotate(listings=Count('raw_listings')))
    ever = {source.slug for source in active if source.listings}
    visited = {result['source'] for result in results}
    ok = [result for result in results if not result['error']]
    blocked = [result for result in results if result['blocked']]
    failed = [result for result in results if result['error'] and not result['blocked']]
    productive = [result for result in ok if result['new'] or result['updated']]
    pages = sum(result['pages'] for result in results)
    minutes = (finished - started).total_seconds() / 60

    lines = [f"# Collect report, {started.astimezone():%Y-%m-%d %H:%M}", '']
    if run['filtered'] or len(visited) < len(active):
        lines += [
            f"> **Partial run: {len(visited)} of {len(active)} active sources were visited**"
            + (' (`--source` filter).' if run['filtered'] else '.'), '',
        ]
    lines += [
        '## Collect', '',
        '| | |', '|---|---|',
        f'| Active sources | {len(active)} |',
        f'| Visited this run | {len(visited)} |',
        f'| Reached | {len(ok)} |',
        f"| Blocked by the work network's filter | {len(blocked)} |",
        f'| Failed | {len(failed)} |',
        f'| Pages fetched | {pages} ({pages / max(len(ok), 1):.1f} per reached source) |',
        f'| Sources with new or changed content | {len(productive)} |',
        f"| New listings | {sum(result['new'] for result in results)} |",
        f"| Changed listings (sent back to extraction) | {sum(result['updated'] for result in results)} |",
        f'| Duration | {minutes:.0f} min |',
        f'| Active sources that have ever produced a listing | {len(ever)} of {len(active)} ({100 * len(ever) / max(len(active), 1):.0f}%) |',
        '',
        '### By group', '',
        '| Group | Active | Visited | Reached | With new content | Pages | Never produced anything |',
        '|---|---|---|---|---|---|---|',
    ]
    by_slug = {result['source']: result for result in results}
    for group in [*GROUPS.values(), NAMED]:
        members = [source for source in active if _group(source.slug) == group]
        group_results = [by_slug[source.slug] for source in members if source.slug in by_slug]
        lines.append(
            f"| {group} | {len(members)} | {len(group_results)} "
            f"| {sum(1 for result in group_results if not result['error'])} "
            f"| {sum(1 for result in group_results if result['new'] or result['updated'])} "
            f"| {sum(result['pages'] for result in group_results)} "
            f"| {sum(1 for source in members if source.slug not in ever)} |"
        )
    top = sorted(productive, key=lambda result: (-result['new'], -result['updated']))[:15]
    if top:
        lines += ['', '### Most new content', '', '| Source | New | Changed | Pages |', '|---|---|---|---|']
        lines += [f"| {r['source']} | {r['new']} | {r['updated']} | {r['pages']} |" for r in top]
    if failed:
        lines += ['', '### Failed', '', '| Source | Error |', '|---|---|']
        lines += [f"| {r['source']} | {r['error'][:150].replace('|', '/')} |" for r in failed]
    silent = sorted(result['source'] for result in ok if result['source'] not in ever)
    lines += _details(f'Reached, but never produced a listing ({len(silent)})', silent)
    lines += _details(
        f"Blocked by the work network's filter ({len(blocked)})", sorted(r['source'] for r in blocked)
    )
    missed = sorted(source.slug for source in active if source.slug not in visited)
    lines += _details(f'Active but not visited this run ({len(missed)})', missed)
    lines += ['', *extraction_section(started, visited, run.get('last_action_id') or 0)]
    return '\n'.join(lines) + '\n'


def extraction_section(started, visited, last_action_id):
    listings = RawListing.objects.filter(fetched_at__gte=started, source__slug__in=visited)
    extracted = listings.exclude(extracted_at=None)
    pending = listings.filter(extracted_at=None).count()
    skipped = extracted.exclude(skip_reason='')
    created = Action.objects.filter(first_seen_at__gte=started, source__slug__in=visited)
    reseen = Action.objects.filter(pk__lte=last_action_id, last_seen_at__gte=started).count()
    # Older listings extracted in the same session (a backlog) also create actions; count them apart.
    backlog = RawListing.objects.filter(extracted_at__gte=started, fetched_at__lt=started).count()
    backlog_actions = Action.objects.filter(pk__gt=last_action_id, first_seen_at__lt=started).count()
    lines = ['## Extraction', '']
    if not listings.exists():
        return lines + ['Nothing new to extract from this run.']
    if pending:
        lines += [f'> **{pending} listing(s) from this run are not extracted yet.** Run `/extract`, then `run_report`.', '']
    pillars = Counter(created.values_list('pillar', flat=True))
    lines += [
        '| | |', '|---|---|',
        f'| Listings to extract from this run | {listings.count()} |',
        f'| Extracted | {extracted.count()} |',
        f'| Not extracted yet | {pending} |',
        f'| Turned into actions | {extracted.filter(skip_reason="").count()} |',
        f'| Skipped | {skipped.count()} |',
        f'| New actions (pending review) | {created.count()} |',
        f'| Already-known actions seen again | {reseen} |',
        f'| Older listings extracted since this run started | {backlog} |',
        f'| New actions from those older listings | {backlog_actions} |',
        f"| New actions by pillar | {', '.join(f'{p}: {n}' for p, n in pillars.most_common()) or 'none'} |",
        f"| Sources that gave a new action | {created.values('source').distinct().count()} |",
    ]
    reasons = Counter(skipped.values_list('skip_reason', flat=True)).most_common(10)
    if reasons:
        lines += ['', '### Main skip reasons', '', '| Reason | Listings |', '|---|---|']
        lines += [f"| {reason.replace('|', '/')} | {count} |" for reason, count in reasons]
    return lines


def _group(slug):
    return GROUPS.get(slug[:3], NAMED)


def _details(summary, items):
    if not items:
        return []
    return ['', f'<details><summary>{summary}</summary>', '', ', '.join(items), '', '</details>']
