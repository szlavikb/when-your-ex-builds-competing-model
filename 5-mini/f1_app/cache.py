import time
from threading import Lock


class SimpleCache:
    """Thread-safe TTL cache with get_or_load."""

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
