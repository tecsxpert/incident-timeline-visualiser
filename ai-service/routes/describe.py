from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.ai_cache import cache_get, cache_set  
from routes.health import record_time               
import json, os, time                               

describe_bp = Blueprint('describe', __name__)

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ['title', 'severity', 'description', 'affected_systems']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    cached = cache_get("describe", data)
    if cached:
        return jsonify({**cached, "cache_hit": True}), 200

    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'describe_prompt.txt')
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()

    generated_at = datetime.now(timezone.utc).isoformat()
    prompt = prompt_template.format(
        title=data['title'], severity=data['severity'],
        description=data['description'], affected_systems=data['affected_systems'],
        start_time=data.get('start_time', 'Not provided'),
        end_time=data.get('end_time', 'Not provided'),
        generated_at=generated_at
    )

    start = time.time()           
    raw = call_groq(prompt)
    record_time((time.time() - start) * 1000)

    # ↓ CHANGED: return fallback instead of 503
    if raw is None:
        return jsonify({
            "summary": "AI service unavailable. Please review manually.",
            "root_cause": "Unable to determine — AI service unavailable.",
            "impact": "Unknown. Please assess manually.",
            "timeline_highlights": ["AI analysis failed", "Manual review recommended"],
            "generated_at": generated_at,
            "is_fallback": True,
            "cache_hit": False
        }), 200

    try:
        result = json.loads(raw.strip().strip('```json').strip('```').strip())
    except json.JSONDecodeError:
        # ↓ CHANGED: return fallback instead of 500
        return jsonify({
            "summary": "AI returned an invalid response.",
            "root_cause": "Unable to determine — AI response was malformed.",
            "impact": "Unknown. Please assess manually.",
            "timeline_highlights": ["AI response parsing failed", "Manual review recommended"],
            "generated_at": generated_at,
            "is_fallback": True,
            "cache_hit": False
        }), 200

    result['generated_at'] = generated_at
    result['is_fallback'] = False
    result['cache_hit'] = False
    cache_set("describe", data, result)  
    return jsonify(result), 200