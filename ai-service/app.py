from flask import Flask, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "ai-service"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)