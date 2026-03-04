from typing import Optional
from threading import Lock


class AgentState:

    def __init__(self):
        self._lock = Lock()
        self.status: str = "idle"
        self.current_job_id: Optional[str] = None
        self.last_error: Optional[str] = None

    def set_idle(self):
        with self._lock:
            self.status = "idle"
            self.current_job_id = None

    def start_job(self, job_id: str):
        with self._lock:
            self.status = "printing"
            self.current_job_id = job_id
            self.last_error = None

    def finish_job(self):
        with self._lock:
            self.status = "idle"
            self.current_job_id = None

    def fail_job(self, error: str):
        with self._lock:
            self.status = "error"
            self.last_error = error
            self.current_job_id = None

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "status": self.status,
                "current_job_id": self.current_job_id,
                "last_error": self.last_error,
            }


AGENT_STATE = AgentState()
