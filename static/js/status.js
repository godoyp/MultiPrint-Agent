import { apiGet } from "./api.js";

export async function loadStatus() {
    try {
        const data = await apiGet("/health");

        document.getElementById("agent-status").innerText = "🟢 Online";
        document.getElementById("active-printer").innerText = data.printer;
        document.getElementById("agent-port").innerText = data.port;

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
  }
}

export async function loadVersion() {
    try {
        const data = await apiGet("/version");
        document.getElementById("agent-version").innerText = data.version;
    } catch {
        document.getElementById("agent-version").innerText = "N/A";
  }
}
