🧠 Overview

The Focus Meditation Agent is an AI-powered meditation assistant built using:

Flask (Backend)

HTML/CSS (Frontend – Blue/White theme)

Gemini Pro API (LLM responses)

JSON Memory System (Long-Term Memory)

LangGraph-style workflow (Reasoning pipeline)

It guides users through personalized meditation sessions based on their mood, history, and duration.

⭐ Features

✔ Generates customized meditation sessions

✔ Short-Term Memory (STM) per session

✔ Long-Term Memory (LTM) stored in memory.json

✔ LangGraph-inspired flow (Memory → LLM → Save)

✔ Lightweight, stable, dependency-free

✔ No ChromaDB issues

📁 Project Structure
focus_agent/
│
├── frontend/
│   ├── index.html
│   └── styles.css
│
└── backend/
    ├── app.py
    ├── langgraph_agent.py
    ├── memory.py
    ├── requirements.txt
    └── .env   <-- You create this

🧠 Memory System
Short-Term Memory (STM)

Lives only during one agent request.
Stored in runtime variables such as:

mood

duration

prompt

mem_results

generated response

Resets on each API call.

Long-Term Memory (LTM)

Stored in memory.json.

Example entry:

{
  "user_id": "abc123",
  "text": "Session summary...",
  "timestamp": 1700000000
}


Used to personalize future sessions.

🚀 Setup Instructions
1. Create Virtual Environment
python -m venv venv


Activate:

venv\Scripts\activate     # Windows

2. Install Dependencies
pip install -r requirements.txt

3. Create .env File

Inside backend/ create:

GEMINI_API_KEY=YOUR_API_KEY_HERE

4. Run Backend
python app.py


Backend available at:

http://127.0.0.1:5000/

🔌 API Endpoint
POST /api/session

Body example:

{
  "mood": "stressed",
  "duration": 5
}


Response example:

GUIDED_SESSION:
Take a slow breath in…

🎨 Frontend

The frontend UI is a clean blue/white theme:

Dropdown for mood

Input for meditation duration

“Start Guided Session” button

Response panel

📦 Requirements

Python 3.10+

Flask

requests

python-dotenv
