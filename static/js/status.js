import { apiGet } from "./api.js";

export async function loadStatus() {
  try {
    const data = await apiGet("/state");

    const statusEl = document.getElementById("agent-status");
    statusEl.textContent = "Agent Online";
    statusEl.className = "badge online";

    document.getElementById("agent-port").textContent = data.port;
    document.getElementById("agent-version").textContent = data.version;

    const httpsEl = document.getElementById("https-status");
    if (window.location.protocol === "https:") {
      httpsEl.textContent = "HTTPS Secure";
      httpsEl.className = "badge online";
    } else {
      httpsEl.textContent = "HTTPS Insecure";
      httpsEl.className = "badge offline";
    }

    const laserEl = document.getElementById("laser-printer");
    const thermalEl = document.getElementById("thermal-printer");

    if (data.printers) {
      if (laserEl) {
        laserEl.textContent = data.printers.laser || "-";
      }

      if (thermalEl) {
        thermalEl.textContent = data.printers.thermal || "-";
      }
    } else {

      if (laserEl) {
        laserEl.textContent = data.printer_name || "-";
      }
      if (thermalEl) {
        thermalEl.textContent = "-";
      }
    }

  } catch (err) {

    const statusEl = document.getElementById("agent-status");
    statusEl.textContent = "Agent Offline";
    statusEl.className = "badge offline";

    const httpsEl = document.getElementById("https-status");
    httpsEl.textContent = "HTTPS Insecure";
    httpsEl.className = "badge offline";

    document.getElementById("agent-version").textContent = "N/A";
  }
}