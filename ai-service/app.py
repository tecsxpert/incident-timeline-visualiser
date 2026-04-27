from flask import Flask, jsonify
from dotenv import load_dotenv
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp  # ← ADD THIS
import os

load_dotenv()

app = Flask(__name__)

app.register_blueprint(describe_bp, url_prefix='/ai')
app.register_blueprint(recommend_bp, url_prefix='/ai')
app.register_blueprint(generate_report_bp, url_prefix='/ai')  # ← ADD THIS

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "ai-service"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)