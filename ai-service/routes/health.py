import time
from flask import Blueprint, jsonify
from services.cache_client import get_cache

health_bp = Blueprint("health", __name__)
START = time.time()
response_times = []

def record_time(ms):
    response_times.append(ms)
    if len(response_times) > 100:
        response_times.pop(0)

@health_bp.route("/health")
def health():
    try:
        get_cache().ping()
        redis_status = "connected"
    except:
        redis_status = "unavailable"

    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": int(time.time() - START),
        "avg_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0,
        "redis": redis_status
    }), 200