import { handshake } from "./auth.js";
import { loadStatus } from "./status.js";
import { loadPrinters, savePrinter, reloadPrinters, testPrint } from "./printers.js";
import { logStream } from "./logs.js";

function bindEvents() {
    document.getElementById("btn-save")?.addEventListener("click", savePrinter);
    document.getElementById("btn-reload")?.addEventListener("click", reloadPrinters);
    document.getElementById("btn-test-print")?.addEventListener("click", testPrint);
}

window.onload = async () => {
    try {
        await handshake();   // 🔐 cria session token
        logStream();         // 🔐 agora pode abrir SSE

        await loadStatus();
        await loadPrinters();

        bindEvents();
    } catch (err) {
        console.error(err);
        alert("Failed to authenticate with MultiPrint Agent");
    }
};
