from datetime import datetime, timezone

import feedparser

from .base import Listing, html_to_text, matches, page_title


def collect(fetcher, config, known_urls):
    feed = feedparser.parse(fetcher.get(config['feed_url']))
    for entry in feed.entries:
        url = entry.get('link')
        title = entry.get('title', '')
        summary = html_to_text(entry.get('summary', ''))
        if not url or not matches(config.get('keywords'), title, summary):
            continue
        if config.get('fetch_detail'):
            if url in known_urls:
                continue
            html = fetcher.get(url)
            title = title or page_title(html)
            text = html_to_text(html, config.get('detail_selector'))
        else:
            text = summary
        yield Listing(url=url, title=title, text=text, published_at=_published(entry))


def _published(entry):
    parsed = entry.get('published_parsed') or entry.get('updated_parsed')
    return datetime(*parsed[:6], tzinfo=timezone.utc) if parsed else None
