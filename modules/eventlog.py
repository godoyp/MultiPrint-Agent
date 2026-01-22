# import os
# from datetime import datetime

# LOG_DIR = "logs"
# LOG_FILE = os.path.join(LOG_DIR, "agent.log")

# os.makedirs(LOG_DIR, exist_ok=True)

# def log_event(message):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{timestamp}] {message}\n")

import os
from datetime import datetime
import queue

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Fila de logs para SSE
log_queue = queue.Queue()

def log_event(message: str):
    """Log normal no arquivo + adiciona na fila SSE"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    
    # escreve no arquivo
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
    
    # adiciona na fila SSE
    log_queue.put(full_msg)
    print(full_msg)

def event_stream():
    """Generator SSE para logs em tempo real"""
    while True:
        msg = log_queue.get()
        yield f"data: {msg}\n\n"
