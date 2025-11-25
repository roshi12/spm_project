import json
import os
import time

class MemoryStore:
    def __init__(self, path="memory.json"):
        self.path = path

        # Create file if it doesn’t exist
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"memories": []}, f, indent=4)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def add_memory(self, user_id, text):
        data = self.load()
        data["memories"].append({
            "user_id": user_id,
            "text": text,
            "timestamp": int(time.time())
        })
        self.save(data)

    def query(self, user_id, mood=None):
        data = self.load()
        results = []

        for mem in data["memories"]:
            if mem["user_id"] == user_id:
                if mood is None or mood in mem["text"]:
                    results.append(mem["text"])

        return results[-3:]   # return last 3 memories
