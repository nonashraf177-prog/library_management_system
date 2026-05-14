# app/core/redis_client.py
import json
import time
import logging

logger = logging.getLogger("library_app")


class InMemoryCache:
    """
    In-memory cache that mimics Redis interface.
    Replace with redis.Redis(...) when Redis server is available.
    """

    def __init__(self):
        self._store: dict = {}          # key -> value
        self._expiry: dict = {}         # key -> expiry timestamp

    def _is_expired(self, key: str) -> bool:
        exp = self._expiry.get(key)
        if exp is None:
            return False
        return time.time() > exp

    def get(self, key: str):
        if key not in self._store or self._is_expired(key):
            self._store.pop(key, None)
            self._expiry.pop(key, None)
            return None
        return self._store[key]

    def set(self, key: str, value, ex: int = None):
        """ex = expiry in seconds"""
        self._store[key] = value
        if ex:
            self._expiry[key] = time.time() + ex
        else:
            self._expiry.pop(key, None)

    def delete(self, key: str):
        self._store.pop(key, None)
        self._expiry.pop(key, None)

    def flush(self):
        self._store.clear()
        self._expiry.clear()


# Single shared instance (swap with real Redis when ready)
redis_client = InMemoryCache()


# ── helper wrappers ──────────────────────────────────────────────────────────

def cache_get(key: str):
    """Get and deserialize a cached JSON value."""
    raw = redis_client.get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


def cache_set(key: str, value, ex: int = 60):
    """Serialize and cache a value. Default TTL = 60 s."""
    redis_client.set(key, json.dumps(value, default=str), ex=ex)


def cache_delete(key: str):
    redis_client.delete(key)
