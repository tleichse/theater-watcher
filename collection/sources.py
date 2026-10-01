INSTITUTION_KEYWORDS = (
    r'audiç|casting|elenco|candidatura|open call|oficina|workshop|formaç|estágio|masterclass'
    r'|residência|bolsa'
)
TV_NEWS_KEYWORDS = r'casting|elenco|audiç|gravaç|gravar|nova novela|nova série|arranc|figura'

SOURCES = [
    {
        'slug': 'coffeepaste', 'name': 'Coffeepaste', 'tier': 'B', 'method': 'html',
        'url': 'https://www.coffeepaste.com/en/classificados/',
        'adapter': 'coffeepaste',
        'config': {'list_url': 'https://www.coffeepaste.com/en/classificados/'},
    },
    {
        'slug': 'encast', 'name': 'enCAST.pro', 'tier': 'B', 'method': 'html',
        'url': 'https://www.encast.pro/castings/portugal',
        'adapter': 'html_list',
        'config': {
            'list_url': 'https://www.encast.pro/castings/portugal',
            'link_pattern': r'/casting-call/',
        },
    },
    {
        'slug': 'tnsj', 'name': 'Teatro Nacional São João', 'tier': 'A', 'method': 'html',
        'url': 'https://www.tnsj.pt/pt/noticias/',
        'adapter': 'html_list',
        'config': {
            'list_url': 'https://www.tnsj.pt/pt/noticias/',
            'link_pattern': r'/pt/noticias/\d+/',
            'keywords': INSTITUTION_KEYWORDS,
        },
    },
    {
        'slug': 'tndm', 'name': 'Teatro Nacional D. Maria II', 'tier': 'A', 'method': 'html',
        'url': 'https://www.tndm.pt/noticias',
        'adapter': 'html_list',
        'config': {
            'list_url': 'https://www.tndm.pt/noticias',
            'scope': '.field--field_noticias',
            'link_pattern': r'^/[a-z0-9-]+$',
            'keywords': INSTITUTION_KEYWORDS,
        },
    },
    {
        'slug': 'sao-luiz', 'name': 'Teatro São Luiz', 'tier': 'A', 'method': 'api',
        'url': 'https://www.teatrosaoluiz.pt/',
        'adapter': 'wordpress',
        'config': {
            'endpoint': 'https://www.teatrosaoluiz.pt/wp-json/wp/v2/espetaculo',
            'search_terms': ['audição', 'audições', 'open call', 'casting'],
        },
    },
    {
        'slug': 'plural-casting', 'name': 'Plural Entertainment (casting)', 'tier': 'A',
        'method': 'html',
        'url': 'https://pluralentertainment.com/casting-figuracao/atores/',
        'adapter': 'page',
        'config': {'urls': ['https://pluralentertainment.com/casting-figuracao/atores/']},
    },
    {
        'slug': 'plural-news', 'name': 'Plural Entertainment (notícias)', 'tier': 'signal',
        'method': 'rss',
        'url': 'https://pluralentertainment.com/',
        'adapter': 'rss',
        'config': {'feed_url': 'https://pluralentertainment.com/feed/'},
    },
    {
        'slug': 'ica', 'name': 'ICA (filmes produzidos)', 'tier': 'signal', 'method': 'html',
        'url': 'https://ica-ip.pt/',
        'adapter': 'ica',
        'config': {
            'url': 'https://ica-ip.pt/pt/tabelas/filmes-produzidos-{year}/',
            'keywords': r'ficção',
        },
    },
    {
        'slug': 'film-commission', 'name': 'Portugal Film Commission', 'tier': 'signal',
        'method': 'html',
        'url': 'https://portugalfilmcommission.com/noticias/',
        'adapter': 'html_list',
        'config': {
            'list_url': 'https://portugalfilmcommission.com/noticias/',
            'link_pattern': r'/noticias/[^/]+/$',
        },
    },
    {
        'slug': 'atelevisao', 'name': 'A Televisão', 'tier': 'signal', 'method': 'rss',
        'url': 'https://www.atelevisao.com/',
        'adapter': 'rss',
        'config': {'feed_url': 'https://www.atelevisao.com/feed/', 'keywords': TV_NEWS_KEYWORDS},
    },
    {
        'slug': 'zapping', 'name': 'Zapping-TV', 'tier': 'signal', 'method': 'rss',
        'url': 'https://www.zapping-tv.com/',
        'adapter': 'rss',
        'config': {'feed_url': 'https://www.zapping-tv.com/feed/', 'keywords': TV_NEWS_KEYWORDS},
    },
    {
        'slug': 'magg', 'name': 'MAGG', 'tier': 'signal', 'method': 'rss',
        'url': 'https://magg.sapo.pt/tag/casting',
        'adapter': 'rss',
        'config': {'feed_url': 'https://magg.sapo.pt/tag/casting/feed/'},
    },
    {
        'slug': 'dgartes', 'name': 'DGArtes (oportunidades)', 'tier': 'B', 'method': 'rss',
        'url': 'https://www.dgartes.gov.pt/pt/taxonomy/term/123',
        'adapter': 'rss',
        'config': {
            'feed_url': 'https://www.dgartes.gov.pt/pt/taxonomy/term/123/feed',
            'fetch_detail': True,
        },
    },
    {
        'slug': 'gda', 'name': 'Fundação GDA', 'tier': 'A', 'method': 'rss',
        'url': 'https://www.fundacaogda.pt/',
        'adapter': 'rss',
        'config': {'feed_url': 'https://www.fundacaogda.pt/feed/', 'fetch_detail': True},
    },
    {
        'slug': 'act', 'name': 'ACT Escola de Actores', 'tier': 'A', 'method': 'rss',
        'url': 'https://act-escoladeactores.com/act/proximos-workshops/',
        'adapter': 'rss',
        'config': {'feed_url': 'https://act-escoladeactores.com/feed/', 'fetch_detail': True},
    },
    {
        'slug': 'vocare', 'name': 'Conservatório Vocare', 'tier': 'A', 'method': 'html',
        'url': 'https://conservatoriovocare.pt/formacoes',
        'adapter': 'page',
        'config': {
            'urls': [
                'https://conservatoriovocare.pt/formacao-dobragem-animacao',
                'https://conservatoriovocare.pt/formacao-locucao-radio',
            ],
        },
    },
]

BY_SLUG = {source['slug']: source for source in SOURCES}
