import os
from datetime import datetime
import queue
from collections import deque

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")
os.makedirs(LOG_DIR, exist_ok=True)

log_queue = queue.Queue()
log_buffer = deque(maxlen=100) 

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

    log_buffer.append(message) 
    log_queue.put(full_msg)
    print(full_msg)

def event_stream():
    yield "data: Log Stream Initialized\n\n"

    for msg in log_buffer:
        yield f"data: {msg}\n\n"

    while True:
        msg = log_queue.get()
        yield f"data: {msg}\n\n"
