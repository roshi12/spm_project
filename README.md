# 🧘‍♂️ Focus Meditation Agent

An AI-powered meditation assistant built using:

* Flask (Backend)
* HTML/CSS (Frontend – Blue/White theme)
* Gemini Pro API (LLM responses)
* JSON Memory System (Long-Term Memory)
* LangGraph-style workflow (Reasoning pipeline)

---

## 🧠 Overview

The Focus Meditation Agent generates personalized guided meditation sessions based on:

* Mood
* Duration
* Long-term memory (JSON)
* Past meditation summaries

It uses a LangGraph-inspired flow:
Memory → Reasoning → Save → Output

---

## ⭐ Features

✔ Personalized meditation sessions
✔ Short-Term Memory per request
✔ Long-Term Memory stored in `memory.json`
✔ Stable (no ChromaDB issues)
✔ Clean UI (blue/white)
✔ Easy to extend

---

## 📁 Project Structure

```
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
```

---

## 🧠 Memory System

### Short-Term Memory (STM)

Lives only during one session.

Holds:

```
mood
duration
prompt
memory results
agent response
```

---

### Long-Term Memory (LTM)

Stored in:

```
memory.json
```

Example:

```json
{
  "user_id": "abc123",
  "text": "Session summary...",
  "timestamp": 1700000000
}
```

---

## 🚀 Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Activate (Windows):

```bash
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `.env` File

Inside backend/:

```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

---

### 4. Run The Backend

```bash
python app.py
```

Backend:

```
http://127.0.0.1:5000/
```

---

## 🔌 API Endpoint

### POST /api/session

#### Request:

```json
{
  "mood": "stressed",
  "duration": 5
}
```

#### Response:

```
GUIDED_SESSION:
Take a slow breath in…
```

---

## 🎨 Frontend

Includes:

* Mood selector
* Duration input
* Generate button
* Response panel

---

## 📦 Requirements

```
Python 3.10+
Flask
requests
python-dotenv
```

---
