import json, os, time
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from services.groq_client import call_groq
from services.input_sanitizer import sanitize_fields
from routes.health import record_time

generate_report_bp = Blueprint("generate_report", __name__)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "generate_report_prompt.txt")


def fallback_response(incident_data):
    return {
        "title": "Incident Report (Fallback)",
        "summary": "AI service is temporarily unavailable. Please review manually.",
        "overview": f"Incident data: {incident_data[:300]}",
        "key_items": ["AI generation failed — manual review required"],
        "recommendations": ["Retry once the AI service recovers"],
        "is_fallback": True,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    data, err = sanitize_fields(data, ['description', 'incident_id', 'title', 'severity', 'affected_systems', 'start_time', 'end_time'])
    if err:
        return jsonify({"error": err}), 400

    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": "'description' is required"}), 400
    if len(description) > 5000:
        return jsonify({"error": "'description' must not exceed 5000 characters"}), 400

    parts = [f"Description: {description}"]
    for key, label in [("incident_id", "Incident ID"), ("title", "Title"),
                        ("severity", "Severity"), ("affected_systems", "Affected Systems"),
                        ("start_time", "Start Time"), ("end_time", "End Time")]:
        if data.get(key, "").strip():
            parts.append(f"{label}: {data[key].strip()}")

    incident_data_str = "\n".join(parts)

    with open(PROMPT_PATH, "r") as f:
        prompt = f.read().replace("{incident_data}", incident_data_str)

    start = time.time()
    raw = call_groq(prompt)
    record_time((time.time() - start) * 1000)

    if raw is None:
        return jsonify(fallback_response(incident_data_str)), 200

    try:
        cleaned = raw.strip().strip('```json').strip('```').strip()
        report = json.loads(cleaned)
        for key in ("title", "summary", "overview", "key_items", "recommendations"):
            if key not in report:
                raise ValueError(f"Missing key: {key}")
        for field in ("key_items", "recommendations"):
            if not isinstance(report[field], list):
                report[field] = [str(report[field])]
    except (json.JSONDecodeError, ValueError):
        return jsonify(fallback_response(incident_data_str)), 200

    report["is_fallback"] = False
    report["generated_at"] = datetime.now(timezone.utc).isoformat()
    return jsonify(report), 200