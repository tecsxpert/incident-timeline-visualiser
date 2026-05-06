from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import logging
import time
from services.groq_client import GroqClient
from services.sanitizer import sanitize_input
from services.prompt_guard import is_prompt_injection

groq_client = GroqClient()
# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

# Logging setup
logging.basicConfig(level=logging.INFO)


# 🔐 Security Headers
@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Server"] = "SecureServer"
    return response


# 🏠 Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Backend Service Running"
    })


# ❤️ Health Endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "AI Backend Running"
    })


# 🤖 AI Endpoint
@app.route("/ask_ai", methods=["POST"])
@limiter.limit("5 per minute")
def ask_ai():

    data = request.get_json()

    # Validate request
    if not data or "prompt" not in data:
        return jsonify({
            "error": "Prompt is required"
        }), 400

    user_input = data["prompt"]

    # Empty input check
    if not user_input.strip():
        return jsonify({
            "error": "Prompt cannot be empty"
        }), 400

    logging.info(f"User Input: {user_input}")

    # ✅ Sanitize input
    clean_input = sanitize_input(user_input)

    # 🚫 Prompt injection detection
    if is_prompt_injection(clean_input):
        logging.warning("Prompt injection attempt blocked")

        return jsonify({
            "error": "Invalid input detected"
        }), 403

    # 🔥 Prompt tuning
    final_prompt = f"""
You are a helpful AI assistant.

Instructions:
- Answer in very simple language
- Keep response short and clear
- Maximum 3 lines
- Avoid complex technical words
- Give beginner-friendly examples if possible

Question:
{clean_input}
"""

    try:
        # ⏱ Response timing
        start = time.time()

        response = groq_client.generate_response(final_prompt)

        end = time.time()

        logging.info(f"Response generated in {end - start:.2f} seconds")

        return jsonify({
            "response": response
        })

    except Exception as e:
        logging.error(f"Error: {str(e)}")

        return jsonify({
            "error": "Failed to generate response"
        }), 500


# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)