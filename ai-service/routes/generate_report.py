import json
import os
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from services.groq_client import call_groq

generate_report_bp = Blueprint("generate_report", __name__)

PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "prompts", "generate_report_prompt.txt"
)


def load_prompt(incident_data: str) -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{incident_data}", incident_data)


def fallback_response(incident_data: str) -> dict:
    return {
        "title": "Incident Report (Fallback)",
        "summary": "AI service is temporarily unavailable. Please review manually.",
        "overview": f"Incident data submitted: {incident_data[:300]}",
        "key_items": ["AI generation failed — manual review required"],
        "recommendations": ["Retry once the AI service recovers"],
        "is_fallback": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@generate_report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": "'description' is required and must not be empty"}), 400

    if len(description) > 5000:
        return jsonify({"error": "'description' must not exceed 5000 characters"}), 400

    # Build context string from all provided fields
    parts = [f"Description: {description}"]
    for key, label in [
        ("incident_id",      "Incident ID"),
        ("title",            "Incident Title"),
        ("severity",         "Severity"),
        ("affected_systems", "Affected Systems"),
        ("start_time",       "Start Time"),
        ("end_time",         "End Time"),
    ]:
        value = data.get(key, "")
        if isinstance(value, str) and value.strip():
            parts.append(f"{label}: {value.strip()}")

    incident_data_str = "\n".join(parts)

    try:
        prompt = load_prompt(incident_data_str)
    except FileNotFoundError:
        return jsonify({"error": "Prompt template not found"}), 500

    raw = call_groq(prompt)

    if raw is None:
        return jsonify(fallback_response(incident_data_str)), 200

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()

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