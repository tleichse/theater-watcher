from . import coffeepaste, html_list, ica, page, rss, wordpress

ADAPTERS = {
    'coffeepaste': coffeepaste.collect,
    'html_list': html_list.collect,
    'ica': ica.collect,
    'page': page.collect,
    'rss': rss.collect,
    'wordpress': wordpress.collect,
}
