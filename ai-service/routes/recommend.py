from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.ai_cache import cache_get, cache_set
from services.input_sanitizer import sanitize_fields
from routes.health import record_time
import json, os, time

recommend_bp = Blueprint('recommend', __name__)

FALLBACK = [
    {"action_type": "Communication", "description": "Notify stakeholders immediately.", "priority": "HIGH"},
    {"action_type": "Monitoring", "description": "Increase monitoring on affected systems.", "priority": "HIGH"},
    {"action_type": "Rollback", "description": "Assess if rollback is possible.", "priority": "MEDIUM"}
]


@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    data, err = sanitize_fields(data, ['title', 'severity', 'affected_systems', 'root_cause'])
    if err:
        return jsonify({"error": err}), 400

    for field in ['title', 'severity', 'affected_systems']:
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

    if raw is None:
        return jsonify({"recommendations": FALLBACK, "is_fallback": True, "cache_hit": False}), 200

    try:
        result = json.loads(raw.strip().strip('```json').strip('```').strip())
    except json.JSONDecodeError:
        return jsonify({"recommendations": FALLBACK, "is_fallback": True, "cache_hit": False}), 200

    if not isinstance(result, list):
        return jsonify({"recommendations": FALLBACK, "is_fallback": True, "cache_hit": False}), 200

    cache_set("recommend", data, {"recommendations": result, "is_fallback": False})
    return jsonify({"recommendations": result, "is_fallback": False, "cache_hit": False}), 200