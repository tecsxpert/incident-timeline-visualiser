from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
import json
import os

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

    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'describe_prompt.txt')
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()

    generated_at = datetime.now(timezone.utc).isoformat()

    prompt = prompt_template.format(
        title=data['title'],
        severity=data['severity'],
        description=data['description'],
        affected_systems=data['affected_systems'],
        start_time=data.get('start_time', 'Not provided'),
        end_time=data.get('end_time', 'Not provided'),
        generated_at=generated_at
    )

    raw = call_groq(prompt)

    if raw is None:
        return jsonify({"error": "AI service unavailable"}), 503

    try:                                  # ← ADD this block
        result = json.loads(raw)
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned invalid response"}), 500

    result['generated_at'] = generated_at
    return jsonify(result), 200