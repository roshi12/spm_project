import os
import json
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langgraph_agent import FocusAgent

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
print("DEBUG APP: GEMINI KEY =", GEMINI_API_KEY)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')

agent = FocusAgent(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/session', methods=['POST'])
def create_session():
    payload = request.get_json() or {}
    mood = payload.get('mood', 'neutral')
    duration = payload.get('duration', 5)
    user_id = payload.get('user_id', 'demo_user')

    try:
        resp = agent.run_guided_session(user_id=user_id, mood=mood, duration=int(duration))
        return jsonify({"success": True, "text": resp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
