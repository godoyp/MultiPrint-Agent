const logsEl = document.getElementById("logs");

export function logStream() {
    if (!logsEl) return;

    const evtSource = new EventSource("/logs/stream");

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
