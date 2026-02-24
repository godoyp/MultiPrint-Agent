import queue
from datetime import datetime
from collections import deque
from multiprint_web_agent.core.paths import LOGS_DIR, AGENT_LOG_PATH
from multiprint_web_agent.core.constants import LOG_BUFFER_SIZE


LOGS_DIR.mkdir(parents=True, exist_ok=True)

log_queue = queue.Queue()
log_buffer = deque(maxlen=LOG_BUFFER_SIZE)

def log_event(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"

    with open(AGENT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

    log_buffer.append(full_msg)
    log_queue.put(full_msg)

    print(full_msg)

def event_stream():
    yield "data: Log Stream Initialized\n\n"

    for msg in log_buffer:
        yield f"data: {msg}\n\n"

    while True:
        msg = log_queue.get()
        yield f"data: {msg}\n\n"
