from datetime import datetime, timedelta, timezone

from .base import Listing, html_to_text

LOOKBACK = timedelta(days=120)


def collect(fetcher, config, known_urls):
    after = (datetime.now(timezone.utc) - LOOKBACK).strftime('%Y-%m-%dT%H:%M:%S')
    seen = set()
    for term in config['search_terms']:
        posts = fetcher.get_json(
            config['endpoint'], search=term, after=after, per_page=20,
            _fields='date_gmt,link,title,content',
        )
        for post in posts:
            if post['link'] in seen:
                continue
            seen.add(post['link'])
            yield Listing(
                url=post['link'],
                title=html_to_text(post['title']['rendered']),
                text=html_to_text(post['content']['rendered']),
                published_at=datetime.fromisoformat(post['date_gmt']).replace(tzinfo=timezone.utc),
            )
