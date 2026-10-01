import html
import json
import re
from datetime import datetime

from .base import Listing, html_to_text

BUNDLE_URL = re.compile(r'https://cdn\.bndlyr\.com/[^"]+/_p/content\.[^"]+\.js[^"]*')
CONTACT = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+351)?\s?\d{3}\s?\d{3}\s?\d{3}')
LISTING_URL = 'https://www.coffeepaste.com/en/classificado/{}/'
FIELDS = [
    ('text_name', 'Publicado por'),
    ('text_sponsor', 'Entidade'),
    ('text_address', 'Morada'),
    ('text_display_event_date', 'Datas'),
    ('text_registration_deadline', 'Prazo (texto)'),
    ('datetime_registration_deadline', 'Prazo'),
    ('text_remuneration', 'Remuneração'),
    ('text_price', 'Preço'),
    ('text_target', 'Destinatários'),
    ('text_how_to_sign_up', 'Como se inscrever'),
]


def collect(fetcher, config, known_urls):
    page = fetcher.get(config['list_url'])
    bundle = fetcher.get(BUNDLE_URL.search(page).group(0))
    content = json.loads(bundle[bundle.index('=') + 1:].strip().rstrip(';'))
    seen = set()
    for repeater in content.values():
        if not isinstance(repeater, dict):
            continue
        related = repeater.get('related') or {}
        for item in repeater.get('items', []):
            if 'datetime_publication_date' not in item:
                continue
            url = LISTING_URL.format(_value(item['_slug']))
            if url in seen:
                continue
            seen.add(url)
            yield Listing(
                url=url,
                title=_value(item['_title']),
                text=_text(item, related),
                published_at=datetime.fromisoformat(item['datetime_publication_date']),
            )


def _text(item, related):
    lines = [
        f"Categoria: {_related_title(related, item.get('ref_category'))}",
        f"Local: {_related_title(related, item.get('ref_place'))}",
    ]
    for key, label in FIELDS:
        value = _value(item.get(key))
        if value:
            lines.append(f'{label}: {value}')
    lines.append('')
    lines.append(html_to_text(_value(item.get('text_description'))))
    return CONTACT.sub('[contacto removido]', '\n'.join(lines))


def _related_title(related, ref):
    return _value((related.get(ref) or {}).get('_title')) if ref else ''


def _value(field):
    if isinstance(field, dict):
        field = field.get('all', '')
    return html.unescape(str(field or '')).strip()
