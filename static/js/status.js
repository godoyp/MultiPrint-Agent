import { apiGet } from "./api.js";

export async function loadStatus() {
    try {
        const data = await apiGet("/state");

        document.getElementById("agent-status").innerText = "🟢 Online";
        document.getElementById("active-printer").innerText = data.printer_name;
        document.getElementById("agent-port").innerText = data.port;
        document.getElementById("agent-version").innerText = data.version;

        const httpsEl = document.getElementById("https-status");
        if (window.location.protocol === "https:") {
        httpsEl.innerText = "HTTPS Active";
        httpsEl.className = "secure";
        } else {
        httpsEl.innerText = "HTTP";
        httpsEl.className = "insecure";
        }
    } catch {
        document.getElementById("agent-status").innerText = "🔴 Offline";
        document.getElementById("agent-version").innerText = "N/A";
  }
}
