from . import coffeepaste, html_list, ica, page, rss, site_watch, wordpress

ADAPTERS = {
    'coffeepaste': coffeepaste.collect,
    'html_list': html_list.collect,
    'ica': ica.collect,
    'page': page.collect,
    'rss': rss.collect,
    'site_watch': site_watch.collect,
    'wordpress': wordpress.collect,
}
