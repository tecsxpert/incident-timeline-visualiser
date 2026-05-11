import time
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)
START = time.time()
response_times = []


def record_time(ms):
    response_times.append(ms)
    if len(response_times) > 100:
        response_times.pop(0)


@health_bp.route("/health")
def health():
    redis_status = "unavailable"
    try:
        from services.cache_client import get_cache
        client = get_cache()
        if client is not None:
            client.ping()
            redis_status = "connected"
    except Exception:
        redis_status = "unavailable"

    avg = round(sum(response_times) / len(response_times), 2) if response_times else 0

    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": int(time.time() - START),
        "avg_response_time_ms": avg,
        "redis": redis_status
    }), 200