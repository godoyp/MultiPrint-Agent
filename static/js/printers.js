import { apiGet, apiPost, apiPut } from "./api.js";
import { showToast } from "./toasts.js";
import { loadStatus } from "./status.js";

const thermalSelect = document.getElementById("thermal-printers");
const laserSelect = document.getElementById("laser-printers");

function addNoneOption(select) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "— None —";
    select.appendChild(opt);
}

export async function loadPrinters() {
    try {
        const printers = await apiGet("/printers/classified");
        const state = await apiGet("/state");

        thermalSelect.innerHTML = "";
        laserSelect.innerHTML = "";

        addNoneOption(thermalSelect);
        addNoneOption(laserSelect);

        printers.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.name;
            opt.textContent = p.name;

            if (p.type === "thermal") {
                if (state.printers && p.name === state.printers.thermal) {
                    opt.selected = true;
                }
                thermalSelect.appendChild(opt);
            }

            if (p.type === "laser") {
                if (state.printers && p.name === state.printers.laser) {
                    opt.selected = true;
                } else if (!state.printers && p.name === state.printer_name) {
                    opt.selected = true;
                }
                laserSelect.appendChild(opt);
            }
        });

    } catch (err) {
        console.error(err);
        showToast("Failed to load printers", "error");
    }
}

export async function savePrinter() {
    const thermal = thermalSelect.value || null;
    const laser = laserSelect.value || null;

    try {
        await apiPut("/printer", {
            role: "thermal",
            printer: thermal
        });

        await apiPut("/printer", {
            role: "laser",
            printer: laser
        });

        showToast("Printers configured successfully", "success");
        await loadStatus();

    } catch (err) {
        console.error(err);
        showToast("Error: Select printer failed", "error");
    }
}

export async function reloadPrinters() {
    showToast("Reloading Printer List...", "info", 2000);
    await loadPrinters();
    showToast("Printer List Updated", "success", 2000);
}

export async function testPrint() {
  showToast("Sending Print Test...", "info", 2000);

  try {
    const res = await fetch("/test-print", { method: "POST" });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.error || "Print test failed");
    }

    showToast("Print Test Successful", "success");
  } catch (err) {
    showToast(`Print Test Failed`, "error");
  }
}
