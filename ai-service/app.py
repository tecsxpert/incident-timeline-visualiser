from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp  # ← add this
import os

load_dotenv()

app = Flask(__name__)

app.register_blueprint(describe_bp, url_prefix='/ai')
app.register_blueprint(recommend_bp, url_prefix='/ai')
app.register_blueprint(generate_report_bp, url_prefix='/ai')
app.register_blueprint(health_bp)  # ← add this (no prefix)

# ← remove the old @app.route('/health') function entirely

if __name__ == '__main__':
    app.run(port=5000, debug=True)