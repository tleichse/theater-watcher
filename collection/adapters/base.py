import re
from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup

TEXT_LIMIT = 10000
NOISE_TAGS = ['script', 'style', 'noscript', 'nav', 'header', 'footer', 'form', 'iframe', 'svg']


@dataclass
class Listing:
    url: str
    title: str
    text: str
    published_at: datetime | None = None


def html_to_text(html, selector=None):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    root = (soup.select_one(selector) if selector else None) or soup.find('main') or soup.find('article') or soup.body or soup
    lines = (line.strip() for line in root.get_text('\n').splitlines())
    return '\n'.join(line for line in lines if line)[:TEXT_LIMIT]


def page_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h1')
    if heading and heading.get_text(strip=True):
        return heading.get_text(' ', strip=True)
    return soup.title.get_text(strip=True) if soup.title else ''


def matches(keywords, *texts):
    if not keywords:
        return True
    return any(re.search(keywords, text or '', re.IGNORECASE) for text in texts)
