from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp
from services.embeddings_service import load_model, init_chroma
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = Flask(__name__)

# Global rate limit: 30 requests per minute per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri=f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}"
)

app.register_blueprint(describe_bp, url_prefix='/ai')
app.register_blueprint(recommend_bp, url_prefix='/ai')
app.register_blueprint(generate_report_bp, url_prefix='/ai')
app.register_blueprint(health_bp)


@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'none'"
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Cache-Control'] = 'no-store'
    response.headers.pop('Server', None)
    return response


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "Too many requests. Try again later."}), 429

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "An internal error occurred."}), 500


# Pre-load model and ChromaDB at startup (Day 11 task)
with app.app_context():
    load_model()
    init_chroma()


if __name__ == '__main__':
    app.run(port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")