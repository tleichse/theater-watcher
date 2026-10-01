from django.utils import timezone
from django.utils.text import slugify

from bs4 import BeautifulSoup

from .base import Listing, matches


def collect(fetcher, config, known_urls):
    url = config['url'].format(year=timezone.now().year)
    table = BeautifulSoup(fetcher.get(url), 'html.parser').find('table')
    rows = table.find_all('tr') if table else []
    if not rows:
        return
    header = rows[0].get_text(' | ', strip=True)
    for row in rows[1:]:
        cells = [cell.get_text(' ', strip=True) for cell in row.find_all(['td', 'th'])]
        line = ' | '.join(cells)
        if len(cells) < 3 or not matches(config.get('keywords'), line):
            continue
        film = cells[-3]
        yield Listing(url=f'{url}#{slugify(film)}', title=film, text=f'{header}\n{line}')
