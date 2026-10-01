from .base import Listing, html_to_text, page_title


def collect(fetcher, config, known_urls):
    for url in config['urls']:
        html = fetcher.get(url)
        yield Listing(url=url, title=page_title(html), text=html_to_text(html, config.get('detail_selector')))
