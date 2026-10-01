import time
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import requests
from django.conf import settings

MIN_DELAY = 1.0
TIMEOUT = 30


class Disallowed(Exception):
    pass


class Fetcher:
    def __init__(self, session=None, sleep=time.sleep, clock=time.monotonic):
        self.session = session or requests.Session()
        self.session.headers['User-Agent'] = settings.COLLECTOR_USER_AGENT
        self.sleep = sleep
        self.clock = clock
        self._robots = {}
        self._last_request = {}

    def get(self, url, **params):
        response = self._request('GET', url, params=params or None)
        # With no charset in the header, requests assumes ISO-8859-1, which garbles UTF-8 pages
        # (JAT and A Oficina declare UTF-8 only in a <meta> tag).
        if 'charset' not in response.headers.get('Content-Type', '').lower() and is_utf8(response.content):
            response.encoding = 'utf-8'
        return response.text

    def get_json(self, url, **params):
        return self._request('GET', url, params=params or None).json()

    def _request(self, method, url, **kwargs):
        origin = self._origin(url)
        robots = self._robots_for(origin)
        if not robots.can_fetch(settings.COLLECTOR_USER_AGENT, url):
            raise Disallowed(url)
        self._wait(origin, robots)
        response = self.session.request(method, url, timeout=TIMEOUT, **kwargs)
        self._last_request[origin] = self.clock()
        response.raise_for_status()
        return response

    def _wait(self, origin, robots):
        delay = max(MIN_DELAY, robots.crawl_delay(settings.COLLECTOR_USER_AGENT) or 0)
        last = self._last_request.get(origin)
        if last is not None:
            remaining = delay - (self.clock() - last)
            if remaining > 0:
                self.sleep(remaining)

    def _robots_for(self, origin):
        if origin not in self._robots:
            parser = RobotFileParser(f'{origin}/robots.txt')
            response = self.session.get(f'{origin}/robots.txt', timeout=TIMEOUT)
            self._last_request[origin] = self.clock()
            # RFC 9309: a missing robots.txt allows everything; a server error disallows everything.
            if response.status_code >= 500:
                parser.disallow_all = True
            elif response.status_code >= 400:
                parser.allow_all = True
            else:
                parser.parse(response.text.splitlines())
            parser.modified()
            self._robots[origin] = parser
        return self._robots[origin]

    @staticmethod
    def _origin(url):
        parts = urlsplit(url)
        return f'{parts.scheme}://{parts.netloc}'


def is_utf8(content):
    try:
        content.decode('utf-8')
    except UnicodeDecodeError:
        return False
    return True
