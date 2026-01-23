import { apiGet, apiPost } from "./api.js";
import { showToast } from "./toasts.js";
import { loadStatus } from "./status.js";

const printersEl = document.getElementById("printers");

export async function loadPrinters() {
    const printers = await apiGet("/printers");
    const config = await apiGet("/config");

    printersEl.innerHTML = "";

    printers.forEach(printer => {
        const opt = document.createElement("option");
        opt.value = printer;
        opt.textContent = printer;

        if (printer === config.printer_name) {
            opt.selected = true;
        }

        printersEl.appendChild(opt);
    });
}

export async function savePrinter() {
    const printer = printersEl.value;

    try {
        await apiPost("/config/printer", { printer });
        showToast(`Printer Selected: ${printer}`, "success");
        await loadStatus();
    } catch {
        showToast("Error: Select printer failed", "error");
    }
}

export async function reloadPrinters() {
    showToast("Reloading Printer List...", "info", 2000);
    await loadPrinters();
    showToast("Printer List Updated", "success", 2000);
}

export async function testPrint() {
    showToast("Sending Print Test...", "info", 3000);

    try {
        await apiPost("/test-print");
        showToast("Print Test Successful", "success");
    } catch {
        showToast("Print Test Failed", "error");
    }
}
