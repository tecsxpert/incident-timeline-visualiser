import hashlib
import json
import logging
from services.cache_client import get_cache

logger = logging.getLogger(__name__)

CACHE_TTL = 900  # 15 minutes


def _make_key(endpoint: str, data: dict) -> str:
    raw = endpoint + json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def cache_get(endpoint: str, data: dict):
    try:
        client = get_cache()
        if client is None:
            return None
        key = _make_key(endpoint, data)
        value = client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.warning(f"Cache GET failed: {e}")
    return None


def cache_set(endpoint: str, data: dict, result: dict):
    try:
        client = get_cache()
        if client is None:
            return
        key = _make_key(endpoint, data)
        client.set(key, json.dumps(result), ex=CACHE_TTL)
    except Exception as e:
        logger.warning(f"Cache SET failed: {e}")