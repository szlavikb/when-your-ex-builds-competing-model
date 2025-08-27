from flask import Flask, render_template, jsonify
import requests
import time
from threading import Lock
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

try:
    import feedparser
    HAVE_FEEDPARSER = True
except Exception:
    feedparser = None
    HAVE_FEEDPARSER = False


class SimpleCache:
    def __init__(self, ttl=120):
        self._store = {}
        self._lock = Lock()
        self.ttl = ttl

    def get_or_load(self, key, loader):
        now = time.time()
        with self._lock:
            entry = self._store.get(key)
            if entry and now - entry['ts'] < self.ttl:
                return entry['val']
        val = loader()
        with self._lock:
            self._store[key] = {'val': val, 'ts': time.time()}
        return val


class FeedAggregator:
    def __init__(self, feeds, timeout=8, max_items=50):
        self.feeds = feeds
        self.timeout = timeout
        self.max_items = max_items

    def _parse_rss_text(self, text):
        items = []
        try:
            root = ET.fromstring(text)
        except Exception:
            return items
        for item in root.findall('.//item'):
            title = item.findtext('title') or ''
            link = item.findtext('link') or ''
            summary = item.findtext('description') or ''
            pub = item.findtext('pubDate') or ''
            items.append({'title': title, 'link': link, 'summary': summary, 'published': pub})
        if not items:
            for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                title = entry.findtext('{http://www.w3.org/2005/Atom}title') or ''
                link_el = entry.find('{http://www.w3.org/2005/Atom}link')
                link = link_el.get('href') if link_el is not None else ''
                summary = entry.findtext('{http://www.w3.org/2005/Atom}summary') or entry.findtext('{http://www.w3.org/2005/Atom}content') or ''
                pub = entry.findtext('{http://www.w3.org/2005/Atom}updated') or entry.findtext('{http://www.w3.org/2005/Atom}published') or ''
                items.append({'title': title, 'link': link, 'summary': summary, 'published': pub})
        return items

    def _to_ts(self, pub_val):
        if not pub_val:
            return 0
        # if feedparser provided a struct_time
        try:
            import time as _time
            if hasattr(pub_val, 'tm_year'):
                return _time.mktime(pub_val)
        except Exception:
            pass
        # string -> try parse
        try:
            dt = parsedate_to_datetime(pub_val)
            return dt.timestamp()
        except Exception:
            return 0

    def fetch(self):
        items = []
        for feed in self.feeds:
            try:
                if HAVE_FEEDPARSER and feedparser is not None:
                    parsed = feedparser.parse(feed)
                    source = getattr(parsed.feed, 'get', lambda k, d=None: parsed.feed.get(k, d))('title', feed) if isinstance(parsed.feed, dict) or hasattr(parsed.feed, 'get') else feed
                    for e in parsed.entries:
                        published = e.get('published', '') if isinstance(e, dict) else getattr(e, 'published', '')
                        published_parsed = e.get('published_parsed') if isinstance(e, dict) else getattr(e, 'published_parsed', None)
                        ts = self._to_ts(published_parsed or published)
                        items.append({
                            'title': e.get('title') or getattr(e, 'title', ''),
                            'link': e.get('link') or getattr(e, 'link', ''),
                            'summary': e.get('summary', '') or getattr(e, 'summary', ''),
                            'published': published,
                            'published_ts': ts,
                            'source': source
                        })
                else:
                    r = requests.get(feed, timeout=self.timeout)
                    if r.status_code == 200:
                        parsed_items = self._parse_rss_text(r.text)
                        for e in parsed_items:
                            ts = self._to_ts(e.get('published'))
                            e['published_ts'] = ts
                            e['source'] = feed
                            items.append(e)
            except Exception:
                continue
        # dedupe by link
        seen = set()
        uniq = []
        for it in items:
            if not it.get('link') or it.get('link') in seen:
                continue
            seen.add(it.get('link'))
            uniq.append(it)
        uniq.sort(key=lambda x: x.get('published_ts', 0) or 0, reverse=True)
        return uniq[: self.max_items]


class StandingsFetcher:
    DRIVER_URL = 'http://ergast.com/api/f1/current/driverStandings.json'
    CONSTRUCTOR_URL = 'http://ergast.com/api/f1/current/constructorStandings.json'

    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch(self):
        out = {}
        try:
            drv = requests.get(self.DRIVER_URL, timeout=self.timeout).json()
            cons = requests.get(self.CONSTRUCTOR_URL, timeout=self.timeout).json()
            out['drivers'] = drv['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            out['constructors'] = cons['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        except Exception:
            out['drivers'] = []
            out['constructors'] = []
        return out


# Application wiring
app = Flask(__name__, static_folder='static', template_folder='templates')
cache = SimpleCache(ttl=120)
aggregator = FeedAggregator([
    'https://www.planetf1.com/feed/',
    'https://www.autosport.com/feed/',
    'https://www.motorsport.com/rss/all/',
])
standings = StandingsFetcher()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/news')
def api_news():
    data = cache.get_or_load('news', aggregator.fetch)
    return jsonify({'items': data})


@app.route('/api/standings')
def api_standings():
    data = cache.get_or_load('standings', standings.fetch)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
