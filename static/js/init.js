import { loadStatus, loadVersion } from "./status.js";
import { loadPrinters, savePrinter, reloadPrinters, testPrint } from "./printers.js";
import { logStream } from "./logs.js";

function bindEvents() {
    document.getElementById("btn-save")?.addEventListener("click", savePrinter);

    document.getElementById("btn-reload")?.addEventListener("click", reloadPrinters);

    document.getElementById("btn-test-print")?.addEventListener("click", testPrint);
}

window.onload = () => {
    loadStatus();
    loadPrinters();
    loadVersion();
    logStream();
    bindEvents();
};
