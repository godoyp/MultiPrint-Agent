import { getSessionToken } from "./auth.js";

const logsEl = document.getElementById("logs");

export function logStream() {
    if (!logsEl) return;

    const token = getSessionToken();
    if (!token) return;

    const evtSource = new EventSource(
        `/ui/logs/stream?token=${encodeURIComponent(token)}`
    );

    evtSource.onmessage = event => {
        const p = document.createElement("p");
        p.textContent = event.data;
        logsEl.appendChild(p);
        logsEl.scrollTop = logsEl.scrollHeight;
    };

    evtSource.onerror = () => {
        const p = document.createElement("p");
        p.textContent = "⚠️ Log Server Connection lost. Trying Again...";
        logsEl.appendChild(p);
        logsEl.scrollTop = logsEl.scrollHeight;
        evtSource.close();
        setTimeout(logStream, 3000);
    };
}
