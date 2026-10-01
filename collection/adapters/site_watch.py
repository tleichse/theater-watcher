from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

from . import rss
from .base import Listing, html_to_text, matches, page_title

FEED_TYPES = ('application/rss+xml', 'application/atom+xml')


def collect(fetcher, config, known_urls):
    homepage = config['url']
    soup = BeautifulSoup(fetcher.get(homepage), 'html.parser')
    feed = discover_feed(soup, homepage)
    if feed:
        rss_config = {'feed_url': feed, 'keywords': config.get('keywords'), 'fetch_detail': True}
        yield from rss.collect(fetcher, rss_config, known_urls)
        return
    host = urlsplit(homepage).netloc.removeprefix('www.')
    links = {}
    for anchor in soup.find_all('a', href=True):
        url = urljoin(homepage, anchor['href']).split('#')[0]
        if urlsplit(url).netloc.removeprefix('www.') == host and url.rstrip('/') != homepage.rstrip('/'):
            links.setdefault(url, anchor.get_text(' ', strip=True))
    for url, anchor_text in links.items():
        if url in known_urls or not matches(config.get('keywords'), anchor_text):
            continue
        try:
            html = fetcher.get(url)
        except requests.HTTPError:
            # One members-only or broken page shouldn't fail the whole site (OUTRO's /portal is a 401).
            continue
        yield Listing(url=url, title=page_title(html) or anchor_text, text=html_to_text(html))


def discover_feed(soup, homepage):
    for link in soup.find_all('link', href=True):
        rel = ' '.join(link.get('rel', [])).lower()
        if 'alternate' in rel and link.get('type') in FEED_TYPES and 'comment' not in link['href'].lower():
            return urljoin(homepage, link['href'])
    return None
