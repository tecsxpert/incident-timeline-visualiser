import os
import logging
import redis

logger = logging.getLogger(__name__)

_client = None


def get_cache():
    global _client

    if _client is False:
        return None

    if _client is not None:
        return _client

    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=0,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2
        )
        client.ping()
        _client = client
        logger.info("Redis connected successfully.")
        return _client
    except Exception as e:
        logger.warning(f"Redis not available — running without cache: {e}")
        _client = False
        return None