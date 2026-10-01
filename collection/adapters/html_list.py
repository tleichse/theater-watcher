import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import Listing, html_to_text, matches, page_title


def collect(fetcher, config, known_urls):
    list_url = config['list_url']
    soup = BeautifulSoup(fetcher.get(list_url), 'html.parser')
    scope = soup.select_one(config['scope']) if config.get('scope') else soup
    links = {}
    for anchor in (scope or soup).find_all('a', href=True):
        if re.search(config['link_pattern'], anchor['href']):
            url = urljoin(list_url, anchor['href']).split('#')[0]
            links.setdefault(url, anchor.get_text(' ', strip=True))
    for url, anchor_text in links.items():
        if url in known_urls or not matches(config.get('keywords'), anchor_text):
            continue
        html = fetcher.get(url)
        yield Listing(
            url=url,
            title=page_title(html) or anchor_text,
            text=html_to_text(html, config.get('detail_selector')),
        )
