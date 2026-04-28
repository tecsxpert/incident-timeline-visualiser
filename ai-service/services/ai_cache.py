import hashlib
import json
from services.cache_client import get_cache

TTL = 15 * 60  # 15 minutes

def make_key(endpoint, payload):
    raw = f"{endpoint}:{json.dumps(payload, sort_keys=True)}"
    return "ai:" + hashlib.sha256(raw.encode()).hexdigest()

def cache_get(endpoint, payload):
    try:
        val = get_cache().get(make_key(endpoint, payload))
        return json.loads(val) if val else None
    except:
        return None

def cache_set(endpoint, payload, response):
    try:
        get_cache().setex(make_key(endpoint, payload), TTL, json.dumps(response))
    except:
        pass