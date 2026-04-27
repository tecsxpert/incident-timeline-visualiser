from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
import json
import os

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ['title', 'severity', 'affected_systems']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'recommend_prompt.txt')
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        title=data['title'],
        severity=data['severity'],
        affected_systems=data['affected_systems'],
        root_cause=data.get('root_cause', 'Not provided')
    )

    raw = call_groq(prompt)

    if raw is None:
        return jsonify({"error": "AI service unavailable"}), 503

    try:                                  # ← ADD this block
        result = json.loads(raw)
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned invalid response"}), 500

    if not isinstance(result, list):
        return jsonify({"error": "Unexpected AI response format"}), 500

    return jsonify(result), 200