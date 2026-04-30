from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

from services.groq_client import GroqClient
from services.sanitizer import sanitize_input
from services.prompt_guard import is_prompt_injection

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Restrict CORS (fix ZAP issue)
CORS(app, resources={r"/ask_ai": {"origins": "http://localhost"}})

# ✅ Rate limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# ✅ Initialize AI client
groq_client = GroqClient()

# ✅ SECURITY HEADERS (ZAP FIX)
@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Server"] = "SecureServer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"
    return response

# HOME ROUTE 
@app.route("/")
def home():
    return "AI Service is running"

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

# MAIN API
@app.route("/ask_ai", methods=["POST"])
@limiter.limit("5 per minute")
def ask_ai():
    data = request.get_json(silent=True)

    # ❌ Empty input check
    if not data or "prompt" not in data or not data["prompt"].strip():
        return jsonify({"error": "Prompt is required"}), 400

    user_input = data["prompt"]

    # ✅ Sanitize input
    clean_input = sanitize_input(user_input)

    # 🚨 Prompt injection detection
    if is_prompt_injection(clean_input):
        return jsonify({"error": "Invalid input detected"}), 403

    # 🔥 PROMPT TUNING (Day 6 improvement)
    final_prompt = f"""
You are a helpful AI assistant.

Instructions:
- Answer in very simple language (for beginners)
- Maximum 2 short lines
- Be clear and direct
- Do NOT use complex or technical words
- If possible, give a small real-life example

Question: {clean_input}
"""

    try:
        response = groq_client.generate_response(final_prompt)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": "AI service failed"}), 500


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)