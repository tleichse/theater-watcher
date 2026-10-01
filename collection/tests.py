import json
from datetime import datetime, timedelta, timezone

from django.test import SimpleTestCase, TestCase
from django.utils import timezone as dj_timezone

from catalog.models import Source

from .adapters import coffeepaste, html_list, ica, rss, wordpress
from .collect import collect_source, prune_raw_text, sync_sources
from .http import Disallowed, Fetcher
from .models import RawListing
from .sources import SOURCES


class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f'HTTP {self.status_code}')


class FakeSession:
    def __init__(self, pages):
        self.pages = pages
        self.headers = {}
        self.requested = []

    def get(self, url, timeout=None):
        return self.request('GET', url, timeout=timeout)

    def request(self, method, url, timeout=None, params=None):
        self.requested.append(url)
        status, text = self.pages.get(url, (404, ''))
        return FakeResponse(status, text)


def fetcher_for(pages):
    return Fetcher(session=FakeSession(pages), sleep=lambda seconds: None)


RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>Feed</title>
<item><title>Audições para nova peça</title><link>https://a.pt/1</link>
<description>&lt;p&gt;Procuramos atores&lt;/p&gt;</description>
<pubDate>Wed, 30 Sep 2026 10:00:00 +0000</pubDate></item>
<item><title>Audiências do mês</title><link>https://a.pt/2</link><description>Números</description></item>
</channel></rss>"""


class FetcherTests(SimpleTestCase):
    def test_sends_user_agent_and_respects_robots(self):
        fetcher = fetcher_for({
            'https://a.pt/robots.txt': (200, 'User-agent: *\nDisallow: /private/'),
            'https://a.pt/public': (200, 'ok'),
        })
        self.assertEqual(fetcher.get('https://a.pt/public'), 'ok')
        self.assertIn('theater-watcher', fetcher.session.headers['User-Agent'])
        with self.assertRaises(Disallowed):
            fetcher.get('https://a.pt/private/page')

    def test_missing_robots_allows_and_server_error_blocks(self):
        fetcher = fetcher_for({
            'https://a.pt/page': (200, 'ok'),
            'https://b.pt/robots.txt': (503, ''),
        })
        self.assertEqual(fetcher.get('https://a.pt/page'), 'ok')
        with self.assertRaises(Disallowed):
            fetcher.get('https://b.pt/page')

    def test_waits_for_crawl_delay(self):
        waits = []
        fetcher = Fetcher(
            session=FakeSession({
                'https://a.pt/robots.txt': (200, 'User-agent: *\nCrawl-delay: 10'),
                'https://a.pt/1': (200, 'one'),
                'https://a.pt/2': (200, 'two'),
            }),
            sleep=waits.append,
            clock=lambda: 0.0,
        )
        fetcher.get('https://a.pt/1')
        fetcher.get('https://a.pt/2')
        self.assertEqual(waits, [10, 10])


class AdapterTests(SimpleTestCase):
    def test_rss_filters_by_keyword_and_reads_dates(self):
        fetcher = fetcher_for({'https://a.pt/feed': (200, RSS)})
        listings = list(rss.collect(fetcher, {'feed_url': 'https://a.pt/feed', 'keywords': 'audiç'}, set()))
        self.assertEqual([listing.url for listing in listings], ['https://a.pt/1'])
        self.assertEqual(listings[0].text, 'Procuramos atores')
        self.assertEqual(listings[0].published_at, datetime(2026, 9, 30, 10, tzinfo=timezone.utc))

    def test_rss_detail_fetch_skips_known_urls(self):
        fetcher = fetcher_for({
            'https://a.pt/feed': (200, RSS),
            'https://a.pt/2': (200, '<main><h1>Audiências</h1><p>Texto completo</p></main>'),
        })
        config = {'feed_url': 'https://a.pt/feed', 'fetch_detail': True}
        listings = list(rss.collect(fetcher, config, {'https://a.pt/1'}))
        self.assertEqual([(listing.url, listing.text) for listing in listings], [('https://a.pt/2', 'Audiências\nTexto completo')])

    def test_html_list_scopes_filters_and_fetches_details(self):
        listing_page = """<nav><a href="/menu">Audições menu</a></nav>
        <div class="news"><a href="/noticia-1">Abrem audições</a><a href="/noticia-2">Prémio</a>
        <a href="/noticia-3">Workshop</a></div>"""
        fetcher = fetcher_for({
            'https://t.pt/noticias': (200, listing_page),
            'https://t.pt/noticia-1': (200, '<header>menu</header><main><h1>Abrem audições</h1><p>Até 10 out</p></main>'),
        })
        config = {
            'list_url': 'https://t.pt/noticias', 'scope': '.news', 'link_pattern': r'^/noticia-\d$',
            'keywords': 'audiç|workshop',
        }
        listings = list(html_list.collect(fetcher, config, {'https://t.pt/noticia-3'}))
        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0].url, 'https://t.pt/noticia-1')
        self.assertEqual(listings[0].text, 'Abrem audições\nAté 10 out')

    def test_coffeepaste_reads_bundle_and_removes_contacts(self):
        item = {
            '_slug': {'all': 'procura-se-voz'}, '_title': {'all': 'Voz &amp; locução'},
            'datetime_publication_date': '2026-09-30T11:57:36.869Z', 'ref_category': 'c1', 'ref_place': 'p1',
            'text_name': {'all': 'Valeria'}, 'text_sponsor': {'all': 'Quinza'},
            'text_email': {'all': 'secret@example.org'},
            'text_how_to_sign_up': {'all': 'Enviar para voz@example.org ou 912 345 678'},
            'text_description': {'all': 'Procuramos vozes.<br/>Pagamento por minuto.'},
        }
        bundle = 'window.BndLyrContent = ' + json.dumps({
            'r1': {'items': [item], 'related': {'c1': {'_title': {'all': 'Oportunidade'}}, 'p1': {'_title': {'all': 'Lisboa'}}}},
            'r2': {'items': [item], 'related': {}},
            'other': {'items': [{'_slug': {'all': 'page'}}]},
        }) + ';'
        bundle_url = 'https://cdn.bndlyr.com/x/_p/content.abc_0.js?v=1'
        fetcher = fetcher_for({
            'https://c.pt/classificados/': (200, f'<script src="{bundle_url}"></script>'),
            bundle_url: (200, bundle),
        })
        listings = list(coffeepaste.collect(fetcher, {'list_url': 'https://c.pt/classificados/'}, set()))
        self.assertEqual(len(listings), 1)
        listing = listings[0]
        self.assertEqual(listing.url, 'https://www.coffeepaste.com/en/classificado/procura-se-voz/')
        self.assertEqual(listing.title, 'Voz & locução')
        for expected in ['Categoria: Oportunidade', 'Local: Lisboa', 'Publicado por: Valeria', 'Entidade: Quinza', 'Pagamento por minuto.']:
            self.assertIn(expected, listing.text)
        for leaked in ['secret@example.org', 'voz@example.org', '912 345 678']:
            self.assertNotIn(leaked, listing.text)

    def test_ica_keeps_matching_rows_with_unique_urls(self):
        table = """<table><tr><th>ANO</th><th>TIPO</th><th>FILME</th><th>REALIZADOR</th><th>PRODUTOR</th></tr>
        <tr><td>2026</td><td>FICÇÃO</td><td>Aquí</td><td>Tiago Guedes</td><td>Leopardo Filmes</td></tr>
        <tr><td>2026</td><td>DOCUMENTÁRIO</td><td>Mar</td><td>X</td><td>Y</td></tr></table>"""
        year = dj_timezone.now().year
        fetcher = fetcher_for({f'https://ica.pt/{year}/': (200, table)})
        listings = list(ica.collect(fetcher, {'url': 'https://ica.pt/{year}/', 'keywords': 'ficção'}, set()))
        self.assertEqual([(listing.url, listing.title) for listing in listings], [(f'https://ica.pt/{year}/#aqui', 'Aquí')])
        self.assertIn('Leopardo Filmes', listings[0].text)

    def test_wordpress_deduplicates_across_search_terms(self):
        post = {'link': 'https://s.pt/open-call', 'date_gmt': '2026-07-14T10:00:00',
                'title': {'rendered': 'Open call'}, 'content': {'rendered': '<p>Audições</p>'}}

        class Session(FakeSession):
            def request(self, method, url, timeout=None, params=None):
                if url.endswith('robots.txt'):
                    return FakeResponse(404, '')
                return FakeResponse(200, json.dumps([post]))

        fetcher = Fetcher(session=Session({}), sleep=lambda seconds: None)
        config = {'endpoint': 'https://s.pt/wp-json/wp/v2/espetaculo', 'search_terms': ['audição', 'open call']}
        listings = list(wordpress.collect(fetcher, config, set()))
        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0].text, 'Audições')


class CollectTests(TestCase):
    def setUp(self):
        sync_sources()
        self.source = Source.objects.get(slug='act')

    def run_with(self, pages):
        return collect_source(self.source, fetcher_for(pages))

    def feed(self, body):
        return {
            'https://act-escoladeactores.com/feed/': (200, RSS.replace('https://a.pt/', 'https://act-escoladeactores.com/')),
            'https://act-escoladeactores.com/1': (200, f'<main>{body}</main>'),
            'https://act-escoladeactores.com/2': (200, '<main>Outro</main>'),
        }

    def test_sync_is_idempotent(self):
        self.assertEqual(sync_sources(), len(SOURCES))
        self.assertEqual(Source.objects.count(), len(SOURCES))

    def test_new_then_unchanged(self):
        self.assertEqual(self.run_with(self.feed('Workshop')).new, 2)
        result = self.run_with(self.feed('Workshop'))
        self.assertEqual((result.new, result.updated, result.error), (0, 0, ''))
        self.assertEqual(RawListing.objects.count(), 2)

    def test_changed_page_is_queued_for_extraction_again(self):
        source = Source.objects.get(slug='vocare')
        pages = {url: (200, '<main>Nível I em setembro</main>') for url in [
            'https://conservatoriovocare.pt/formacao-dobragem-animacao',
            'https://conservatoriovocare.pt/formacao-locucao-radio',
        ]}
        collect_source(source, fetcher_for(pages))
        RawListing.objects.update(extracted_at=dj_timezone.now())
        pages['https://conservatoriovocare.pt/formacao-locucao-radio'] = (200, '<main>Nível I em outubro</main>')
        result = collect_source(source, fetcher_for(pages))
        self.assertEqual(result.updated, 1)
        self.assertEqual(RawListing.objects.filter(extracted_at__isnull=True).count(), 1)

    def test_failure_is_reported_and_keeps_earlier_listings(self):
        pages = self.feed('Workshop')
        del pages['https://act-escoladeactores.com/2']
        result = self.run_with(pages)
        self.assertEqual(result.new, 1)
        self.assertIn('404', result.error)

    def test_prune_clears_old_text_but_keeps_the_url(self):
        self.run_with(self.feed('Workshop'))
        RawListing.objects.filter(url__endswith='/1').update(fetched_at=dj_timezone.now() - timedelta(days=61))
        self.assertEqual(prune_raw_text(), 1)
        pruned = RawListing.objects.get(url__endswith='/1')
        self.assertEqual(pruned.raw_text, '')
        self.assertEqual(self.run_with(self.feed('Changed')).new, 0)
