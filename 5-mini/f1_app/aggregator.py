import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import requests
import os
import traceback


def _append_debug_log(text: str):
    try:
        os.makedirs(os.path.join(os.getcwd(), 'logs'), exist_ok=True)
        with open(os.path.join(os.getcwd(), 'logs', 'debug.log'), 'a', encoding='utf-8') as f:
            f.write(text + "\n\n")
    except Exception:
        # best-effort logging; don't raise
        pass


class FeedAggregator:
    def __init__(self, feeds, timeout=6, max_items=50):
        self.feeds = feeds
        self.timeout = timeout
        self.max_items = max_items
    self.session = requests.Session()
    self.last_error = None
    self.last_fetch = None

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
        try:
            # if struct_time-like
            import time as _time
            if hasattr(pub_val, 'tm_year'):
                return _time.mktime(pub_val)
        except Exception:
            pass
        try:
            dt = parsedate_to_datetime(pub_val)
            return dt.timestamp()
        except Exception:
            return 0

    def fetch(self):
        import time as _time
        items = []
        self.last_error = None
        self.last_fetch = _time.time()
        for feed in self.feeds:
            try:
                r = self.session.get(feed, timeout=self.timeout)
                if r.status_code == 200 and r.text:
                    parsed_items = self._parse_rss_text(r.text)
                    for e in parsed_items:
                        ts = self._to_ts(e.get('published'))
                        e['published_ts'] = ts
                        e['source'] = feed
                        items.append(e)
            except Exception:
                # record the last error but keep going with other feeds
                tb = traceback.format_exc()
                self.last_error = tb
                _append_debug_log('[aggregator] ' + tb)
                continue
        # dedupe
        seen = set()
        uniq = []
        for it in items:
            link = it.get('link')
            if not link or link in seen:
                continue
            seen.add(link)
            uniq.append(it)
        uniq.sort(key=lambda x: x.get('published_ts', 0) or 0, reverse=True)
        return uniq[: self.max_items]
