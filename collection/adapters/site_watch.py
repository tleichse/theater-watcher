import re
from urllib.parse import unquote, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

from ..http import Disallowed
from . import rss
from .base import Listing, html_to_text, matches, page_title

FEED_TYPES = ('application/rss+xml', 'application/atom+xml')
# Sections most likely to hold calls, best first. Calls and training sections are re-read every run
# (a changed page is re-extracted); news sections are only scanned for links.
SECTIONS = (
    (r'audiç|audicoes|casting|oportunidade|open call|opencall|convocat|candidatura|recrutamento', True),
    (r'formaç|formacao|curso|workshop|oficina|residênc|residencia|masterclass', True),
    (r'notícia|noticia|novidade|news|blog|destaque', False),
)
MAX_SECTIONS = 3
REDIRECT = re.compile(
    r'http-equiv=["\']?refresh["\']?\s+content=["\'][^"\']*url=\'?([^"\'>]+)'
    r'|window\.location(?:\.href)?\s*=\s*["\']([^"\']+)',
    re.IGNORECASE,
)


def collect(fetcher, config, known_urls):
    homepage = config['url']
    html = fetcher.get(homepage)
    # A stub that only redirects (Tarumba's homepage sends to /2026/, Baal 17's to /_www/).
    redirect = REDIRECT.search(html) if len(html) < 3000 else None
    if redirect:
        target = urljoin(homepage, redirect.group(1) or redirect.group(2))
        if _host(target) == _host(homepage):
            homepage = target
            html = fetcher.get(homepage)
    soup = BeautifulSoup(html, 'html.parser')
    feed = discover_feed(soup, homepage)
    seen = set(known_urls)
    if feed:
        # Same rule as the followed links below: a dead post skips (SP Entertainment's feed had a 404).
        rss_config = {'feed_url': feed, 'keywords': config.get('keywords'), 'fetch_detail': True, 'skip_failed_detail': True}
        try:
            for listing in rss.collect(fetcher, rss_config, known_urls):
                seen.add(listing.url)
                yield listing
        except requests.HTTPError:
            # The advertised feed is dead (Gulbenkian's and Santa Claus's were); the homepage still is read.
            pass
    # Read the homepage even with a feed: 97 sites had an empty or years-old WordPress feed
    # while their homepage linked current calls.
    links = own_links(soup, homepage)
    # Calls usually sit one level down, in an "Audições" or "Notícias" section, not on the homepage.
    for section, reread in pick_sections(links):
        try:
            section_html = fetcher.get(section)
        except (requests.HTTPError, Disallowed):
            continue
        for url, texts in own_links(BeautifulSoup(section_html, 'html.parser'), section).items():
            links.setdefault(url, []).extend(texts)
        if reread:
            seen.add(section)
            yield Listing(url=section, title=page_title(section_html) or section, text=html_to_text(section_html))
    for url, anchor_texts in links.items():
        # Only the last segment: a whole path matched every page under Jobra's
        # /cursos-profissionais-com-inscricoes-abertas/ section, statutes and accounts included.
        slug = unquote(urlsplit(url).path).rstrip('/').rsplit('/', 1)[-1].replace('-', ' ')
        if url in seen or not matches(config.get('keywords'), *anchor_texts, slug):
            continue
        seen.add(url)
        try:
            html = fetcher.get(url)
        except (requests.HTTPError, Disallowed):
            # One members-only, broken or robots-refused page shouldn't fail the whole site
            # (OUTRO's /portal is a 401; CRIM's robots.txt refuses one regulation page).
            continue
        yield Listing(url=url, title=page_title(html) or max(anchor_texts, key=len), text=html_to_text(html))


def own_links(soup, page):
    links = {}
    for anchor in soup.find_all('a', href=True):
        try:
            url = urljoin(page, anchor['href']).split('#')[0]
            same_site = _host(url) == _host(page)
        except ValueError:
            # Teatro Villaret links to an unrendered WordPress shortcode ("[acf field=…]").
            continue
        if same_site and url.rstrip('/') != page.rstrip('/') and not _is_file(url):
            # A card often links the same page from its image (no text), its title and a "Ler mais";
            # the first anchor alone missed Visões Úteis's open calls.
            links.setdefault(url, []).append(anchor.get_text(' ', strip=True))
    return links


def pick_sections(links):
    picked = []
    for pattern, reread in SECTIONS:
        for url, texts in links.items():
            path = unquote(urlsplit(url).path).strip('/')
            # A section is a short path (one or two segments), not a single post.
            if path.count('/') > 1 or urlsplit(url).query or any(url == p for p, _ in picked):
                continue
            if matches(pattern, *texts, path.replace('-', ' ')):
                picked.append((url, reread))
                break
    return picked[:MAX_SECTIONS]


def _host(url):
    return urlsplit(url).netloc.lower().removeprefix('www.')


def _is_file(url):
    return bool(re.search(r'\.(pdf|jpe?g|png|gif|zip|docx?|mp[34])$', urlsplit(url).path, re.IGNORECASE))


def discover_feed(soup, homepage):
    for link in soup.find_all('link', href=True):
        rel = ' '.join(link.get('rel', [])).lower()
        if 'alternate' in rel and link.get('type') in FEED_TYPES and 'comment' not in link['href'].lower():
            return urljoin(homepage, link['href'])
    return None
