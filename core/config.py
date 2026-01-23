import json

with open("config.json", encoding="utf-8") as f:
    CONFIG = json.load(f)

PORT = CONFIG.get("agent_port", 5000)
