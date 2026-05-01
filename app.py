from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from dotenv import load_dotenv
import os

from services.groq_client import GroqClient
from services.sanitizer import sanitize_input
from services.prompt_guard import is_prompt_injection

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

# Initialize Groq client
groq_client = GroqClient()


# ✅ Home route
@app.route("/")
def home():
    return "Server is running"


# ✅ AI Endpoint
@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()

    # ❌ Empty input check
    if not data or "prompt" not in data or not data["prompt"].strip():
        return jsonify({"error": "Prompt is required"}), 400

    user_input = data["prompt"]

    # ✅ Step 1: Sanitize input
    clean_input = sanitize_input(user_input)

    # ❌ Step 2: Prompt injection detection
    if is_prompt_injection(clean_input):
        return jsonify({"error": "Invalid input detected"}), 403

    # 🔥 Step 3: Prompt tuning (Day 6 improved)
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
        # ✅ Step 4: Call AI
        response = groq_client.generate_response(final_prompt)

        return jsonify({"response": response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "AI service failed"}), 500


# Run server
if __name__ == "__main__":
    app.run(debug=True)