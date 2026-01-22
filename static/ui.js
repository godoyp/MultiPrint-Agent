const printersEl = document.getElementById("printers");
const statusEl = document.getElementById("status");
const logsEl = document.getElementById("logs");

// TOASTS
function showToast(message, type = "info", timeout = 4000) {
  const container = document.getElementById("toast-container");

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerText = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, timeout);
}

// VERSION
async function loadVersion() {
  try {
    const data = await fetch("/version").then(r => r.json());
    document.getElementById("agent-version").innerText = data.version;
  } catch {
    document.getElementById("agent-version").innerText = "N/A";
  }
}

// AGENT STATUS
async function loadStatus() {
  try {
    const data = await fetch("/health").then(r => r.json());
    document.getElementById("agent-status").innerText = "🟢 Online";
    document.getElementById("active-printer").innerText = data.printer;
    document.getElementById("agent-port").innerText = data.port;

    const httpsEl = document.getElementById("https-status");
    if (window.location.protocol === "https:") {
      httpsEl.innerText = "HTTPS Ativo";
      httpsEl.className = "secure";
    } else {
      httpsEl.innerText = "HTTP";
      httpsEl.className = "insecure";
    }
  } catch {
    document.getElementById("agent-status").innerText = "🔴 Offline";
  }
}

// PRINTERS
async function loadPrinters() {
  const printers = await fetch("/printers").then(r => r.json());
  const config = await fetch("/config").then(r => r.json());

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

// SAVE CONFIG
async function savePrinter() {
  const printer = printersEl.value;

  try {
    await fetch("/config/printer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ printer })
    });

    showToast("Impressora atualizada com sucesso", "success");

    await loadStatus();

  } catch {
    showToast("Erro ao salvar impressora", "error");
  }
}

// RELOAD PRINTERS
async function reloadPrinters() {
  showToast("Recarregando impressoras...", "info", 2000);
  await loadPrinters();
  showToast("Lista de impressoras atualizada", "success", 2000);
}


// PRINT TEST
async function testPrint() {
  showToast("Enviando teste de impressão...", "info", 3000);

  try {
    const res = await fetch("/test-print", { method: "POST" });

    if (res.ok) {
      showToast("Teste enviado para a impressora", "success");
    } else {
      showToast("Falha no teste de impressão", "error");
    }
  } catch {
    showToast("Falha no teste de impressão", "error");
  }
}

// REAL-TIME LOGS
function startLogStream() {
  if (!logsEl) return;

  const evtSource = new EventSource("/logs/stream");

  evtSource.onmessage = function(event) {
    const p = document.createElement("p");
    p.textContent = event.data;
    logsEl.appendChild(p);
    logsEl.scrollTop = logsEl.scrollHeight;
  };

  evtSource.onerror = function() {
    const p = document.createElement("p");
    p.textContent = "⚠️ Conexão de logs perdida. Tentando reconectar...";
    logsEl.appendChild(p);
    logsEl.scrollTop = logsEl.scrollHeight;
    evtSource.close();
    setTimeout(startLogStream, 3000);
  };
}

// INIT
window.onload = () => {
  loadStatus();
  loadPrinters();
  startLogStream();
  loadVersion();
};
