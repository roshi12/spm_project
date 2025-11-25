import os
import json
import time
import requests
from memory import MemoryStore

class FocusAgent:
    def __init__(self, api_key: str):
        
        # DEBUG: Added back the debug prints for continuity
        print("DEBUG AGENT INIT - received API KEY =", api_key)
        self.api_key = api_key
        self.mem = MemoryStore()  # JSON Memory
        self.use_stub = not bool(api_key)
        print("DEBUG AGENT INIT - use_stub =", self.use_stub)
        
    # -----------------------
    # Gemini API Caller
    # -----------------------
    def call_gemini(self, prompt: str, temperature: float = 0.3):
        
        # DEBUG: Added back the debug prints for continuity
        print("DEBUG CALL_GEMINI - api_key =", self.api_key[:8] + '...')
        print("DEBUG CALL_GEMINI - use_stub =", self.use_stub)
        
        if self.use_stub:
            return "(GEMINI API KEY MISSING) Guided breathing: Breathe in 4s, hold 4s, out 6s..."

        # FIX: Changed model alias in the URL to the full, unambiguous model name
        # The API alias 'gemini-2.5-flash' works for client libraries but sometimes
        # requires the full path when hitting the raw REST endpoint.
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
        
        # Note: The 'gemini-2.5-flash' alias often routes to the current best version,
        # but using the preview model name is safer for the direct REST API call.

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        full_url = f"{url}?key={self.api_key}"

        # Implementing exponential backoff for robustness
        for i in range(5):
            try:
                r = requests.post(full_url, headers=headers, json=payload, timeout=30)
                r.raise_for_status()
                data = r.json()
                
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except KeyError:
                    # Handle cases where the response is valid JSON but lacks expected fields
                    return f"Error: Unexpected API response structure: {str(data)}"
                
            except requests.exceptions.RequestException as e:
                if r.status_code == 404:
                    return f"ERROR 404: Model not found at specified URL. Check model name. Details: {e}"
                
                # Check for rate limiting (429) or transient server errors (5xx)
                if r.status_code in [429, 500, 503] and i < 4:
                    sleep_time = 2 ** i
                    time.sleep(sleep_time)
                    print(f"Retrying API call after {sleep_time}s due to error: {r.status_code}")
                    continue
                
                return f"ERROR: API request failed. Status: {r.status_code}. Details: {e}"
            except Exception as e:
                return f"An unexpected error occurred during API call: {e}"

        return "ERROR: API call failed after multiple retries."

    # -----------------------
    # Build Prompt
    # -----------------------
    def build_prompt(self, user_id: str, mood: str, duration: int, memory_snippets=None):
        memory_snippets = memory_snippets or []

        base = [
            f"You are a Focus Meditation Agent. Create a {duration}-minute guided meditation for a user feeling {mood}.",
            "Output must start with 'GUIDED_SESSION:'",
        ]

        if memory_snippets:
            base.append("Here is some relevant user memory:\n" + "\n".join(memory_snippets))

        return "\n\n".join(base)

    # -----------------------
    # Main Workflow
    # -----------------------
    def run_guided_session(self, user_id: str, mood: str, duration: int):

        # JSON Memory Query (Long-Term Memory)
        mem_results = []
        try:
            mem_results = self.mem.query(user_id, mood)  # returns last 3
        except Exception:
            mem_results = []

        # Build prompt with memory
        prompt = self.build_prompt(user_id, mood, duration, mem_results)

        # Call Gemini LLM
        text = self.call_gemini(prompt)

        # Save memory to JSON (LTM)
        try:
            self.mem.add_memory(
                user_id,
                f"Session summary (mood={mood}, duration={duration}): {text[:200]}"
            )
        except Exception:
            pass

        return text