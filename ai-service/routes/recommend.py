from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.ai_cache import cache_get, cache_set  
from routes.health import record_time               
import json, os, time                               

recommend_bp = Blueprint('recommend', __name__)

FALLBACK_RECOMMENDATIONS = [
    {"action_type": "Communication", "description": "Notify stakeholders of the incident immediately.", "priority": "HIGH"},
    {"action_type": "Monitoring", "description": "Increase monitoring on affected systems.", "priority": "HIGH"},
    {"action_type": "Rollback", "description": "Assess if rollback to last stable state is possible.", "priority": "MEDIUM"}
]

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ['title', 'severity', 'affected_systems']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    cached = cache_get("recommend", data)
    if cached:
        return jsonify({**cached, "cache_hit": True}), 200

    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'recommend_prompt.txt')
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        title=data['title'], severity=data['severity'],
        affected_systems=data['affected_systems'],
        root_cause=data.get('root_cause', 'Not provided')
    )

    start = time.time()           
    raw = call_groq(prompt)
    record_time((time.time() - start) * 1000)

    # ↓ CHANGED: return fallback instead of 503
    if raw is None:
        return jsonify({"recommendations": FALLBACK_RECOMMENDATIONS, "is_fallback": True, "cache_hit": False}), 200

    try:
        result = json.loads(raw.strip().strip('```json').strip('```').strip())
    except json.JSONDecodeError:
        # ↓ CHANGED: return fallback instead of 500
        return jsonify({"recommendations": FALLBACK_RECOMMENDATIONS, "is_fallback": True, "cache_hit": False}), 200

    if not isinstance(result, list):
        # ↓ CHANGED: return fallback instead of 500
        return jsonify({"recommendations": FALLBACK_RECOMMENDATIONS, "is_fallback": True, "cache_hit": False}), 200

    cache_set("recommend", data, {"recommendations": result, "is_fallback": False})
    return jsonify({"recommendations": result, "is_fallback": False, "cache_hit": False}), 200