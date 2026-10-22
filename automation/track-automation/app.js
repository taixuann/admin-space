/**
 * Track Automation — Client Controller (LifeOS / Bridge Editorial Standard)
 * Matches the layout, typography, and split-layout action studio of Bridge.
 */

const ICONS = {
  check: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`,
  alert: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
  clock: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  terminal: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`,
  copy: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`,
  play: `<svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>`,
};

let appState = {
  automations: [],
  selectedId: null,
  activeFilter: "all",
  searchQuery: "",
  viewMode: "list", // 'list' | 'card'
  isDocsView: false,
};

let toastTimeout = null;

function showToast(msg) {
  const toast = document.getElementById("toast");
  const msgEl = document.getElementById("toastMessage");
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  toast.classList.add("show");
  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2200);
}

function copyToClipboard(text, label = "Command") {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast(`Copied ${label} to clipboard!`);
  }).catch(() => {
    prompt(`Copy ${label}:`, text);
  });
}

function copyScanCommand() {
  const cmd = "assets/track-automation/bin/track-automation status";
  copyToClipboard(cmd, "CLI status command");
}

function toggleDocsView() {
  appState.isDocsView = !appState.isDocsView;
  const splitLayout = document.getElementById("splitLayout");
  const docsView = document.getElementById("docsView");
  const toggleBtnText = document.getElementById("docsBtnText");

  if (appState.isDocsView) {
    splitLayout.style.display = "none";
    docsView.classList.add("active");
    toggleBtnText.textContent = "Back to Automations";
  } else {
    splitLayout.style.display = "grid";
    docsView.classList.remove("active");
    toggleBtnText.textContent = "Runbook & Docs";
  }
}

async function loadData() {
  try {
    const res = await fetch("automations.json", { cache: "no-store" });
    if (res.ok) {
      const data = await res.json();
      initDashboard(data);
      return;
    }
  } catch (err) {
    console.warn("Could not fetch automations.json via HTTP, checking embedded data", err);
  }

  if (window.EMBEDDED_DATA) {
    initDashboard(window.EMBEDDED_DATA);
  } else {
    document.getElementById("listTableContainer").innerHTML = `
      <div style="padding: 40px; text-align: center; color: var(--muted);">
        Could not load automations registry. Run <code>python3 scan_automations.py</code> first.
      </div>
    `;
  }
}

function initDashboard(data) {
  appState.automations = data.automations || [];
  appState.timestamp = data.timestamp || "";

  // Auto-select first item
  if (!appState.selectedId && appState.automations.length > 0) {
    appState.selectedId = appState.automations[0].id;
  }

  updateMetrics();
  renderMain();
  renderStudio();
  setupEventListeners();

  const scanTimeEl = document.getElementById("lastScanTime");
  if (scanTimeEl) {
    scanTimeEl.textContent = `Scanned: ${appState.timestamp.split(" ")[1] || "Just now"}`;
  }
}

function updateMetrics() {
  const autos = appState.automations;
  const total = autos.length;
  const running = autos.filter((a) => a.status_code === "running").length;
  const scheduled = autos.filter((a) => a.status_code === "idle").length;
  const aiCount = autos.filter((a) => a.category === "ai").length;
  const errors = autos.filter((a) => a.status_code === "error" || a.status_code === "malformed").length;

  document.getElementById("totalCount").textContent = total;
  document.getElementById("runningCount").textContent = running;
  document.getElementById("scheduledCount").textContent = scheduled;
  document.getElementById("aiCount").textContent = aiCount;
  document.getElementById("errorCount").textContent = errors;
}

function getFilteredAutomations() {
  return appState.automations.filter((item) => {
    if (appState.activeFilter !== "all" && item.category !== appState.activeFilter) {
      return false;
    }
    if (appState.searchQuery) {
      const q = appState.searchQuery.toLowerCase();
      const match =
        (item.name && item.name.toLowerCase().includes(q)) ||
        (item.label && item.label.toLowerCase().includes(q)) ||
        (item.id && item.id.toLowerCase().includes(q)) ||
        (item.description && item.description.toLowerCase().includes(q)) ||
        (item.schedule && item.schedule.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });
}

function renderMain() {
  const filtered = getFilteredAutomations();
  const listContainer = document.getElementById("listTableContainer");
  const cardsGrid = document.getElementById("cardsGrid");
  const groupLabel = document.getElementById("groupHeaderLabel");

  if (groupLabel) {
    const catName = appState.activeFilter === "all" ? "All Services" : appState.activeFilter.toUpperCase();
    groupLabel.textContent = `${catName} (${filtered.length})`;
  }

  if (appState.viewMode === "list") {
    listContainer.style.display = "flex";
    cardsGrid.classList.remove("active");

    if (filtered.length === 0) {
      listContainer.innerHTML = `
        <div style="padding: 40px; text-align: center; color: var(--muted); font-size: 13px;">
          No automations found matching current filter.
        </div>
      `;
      return;
    }

    listContainer.innerHTML = filtered.map((item) => {
      const isSelected = item.id === appState.selectedId ? "is-selected" : "";
      let badgeClass = "badge-unloaded";
      let statusLabel = item.status;

      if (item.status_code === "running") {
        badgeClass = "badge-running";
      } else if (item.status_code === "idle") {
        badgeClass = "badge-idle";
      } else if (item.status_code === "error" || item.status_code === "malformed") {
        badgeClass = "badge-error";
        statusLabel = item.last_exit_code ? `Exit ${item.last_exit_code}` : "Error";
      }

      const dotColor = item.status_code === "running" ? "#2cb67d" : item.status_code === "idle" ? "#1b538c" : "#963833";

      return `
        <div class="ws-list-row ${isSelected}" onclick="selectItem('${escapeHtml(item.id)}')">
          <div class="ws-list-dot-col">
            <span style="width:7px; height:7px; border-radius:50%; background:${dotColor}; display:inline-block;"></span>
          </div>

          <div class="ws-list-name-col">
            <div class="ws-list-name-row">
              <span class="ws-list-name">${escapeHtml(item.name || item.label)}</span>
              <span class="category-tag cat-${item.category}">${escapeHtml(item.category)}</span>
            </div>
            <span class="ws-list-sub">${escapeHtml(item.id)}</span>
          </div>

          <div class="ws-list-schedule" title="${escapeHtml(item.schedule)}">
            ${ICONS.clock}
            <span>${escapeHtml(item.schedule)}</span>
          </div>

          <div>
            <span class="badge ${badgeClass}">${escapeHtml(statusLabel)}</span>
          </div>

          <div class="ws-list-action-col">
            <button class="action-icon-btn" title="Copy Service ID" onclick="event.stopPropagation(); copyToClipboard('${escapeHtml(item.id)}', 'Service ID')">
              ${ICONS.copy}
            </button>
          </div>
        </div>
      `;
    }).join("");
  } else {
    listContainer.style.display = "none";
    cardsGrid.classList.add("active");

    if (filtered.length === 0) {
      cardsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--muted); font-size: 13px;">
          No automations found matching current filter.
        </div>
      `;
      return;
    }

    cardsGrid.innerHTML = filtered.map((item) => {
      const isSelected = item.id === appState.selectedId ? "is-selected" : "";
      let badgeClass = item.status_code === "running" ? "badge-running" : item.status_code === "idle" ? "badge-idle" : "badge-error";

      return `
        <div class="ws-card ${isSelected}" onclick="selectItem('${escapeHtml(item.id)}')">
          <div class="ws-card-header">
            <span class="ws-card-name">${escapeHtml(item.name || item.label)}</span>
            <span class="badge ${badgeClass}">${escapeHtml(item.status)}</span>
          </div>
          <div style="font-size:11px; font-family:var(--font-mono); color:var(--muted);">${escapeHtml(item.id)}</div>
          <p style="font-size:12.5px; color:var(--muted); line-height:1.4; flex-grow:1;">
            ${escapeHtml(item.description || "Background service.")}
          </p>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:11.5px; border-top:1px solid rgba(0,0,0,0.05); padding-top:8px;">
            <span class="category-tag cat-${item.category}">${escapeHtml(item.category)}</span>
            <span style="color:var(--muted);">${escapeHtml(item.schedule)}</span>
          </div>
        </div>
      `;
    }).join("");
  }
}

function selectItem(id) {
  appState.selectedId = id;
  renderMain();
  renderStudio();
}

function renderStudio() {
  const studioCard = document.getElementById("studioCard");
  const item = appState.automations.find((a) => a.id === appState.selectedId);

  if (!item) {
    studioCard.innerHTML = `
      <div style="text-align: center; padding: 60px 20px; color: var(--muted); font-size: 13px;">
        Select an automation on the left to inspect runbook actions, live status, and execution logs.
      </div>
    `;
    return;
  }

  let badgeClass = item.status_code === "running" ? "badge-running" : item.status_code === "idle" ? "badge-idle" : "badge-error";

  // Dynamic Runbook Commands
  let kickstartCmd = `launchctl kickstart -k gui/$(id -u)/${item.label || item.id}`;
  let reloadCmd = item.plist_path ? `launchctl unload ${item.plist_path} && launchctl load -w ${item.plist_path}` : "";
  let lintCmd = item.plist_path ? `plutil -lint ${item.plist_path}` : "";
  let logCmd = item.stdout_log?.path ? `tail -n 50 -f ${item.stdout_log.path}` : "";

  // Special command blocks for Bridge & Model Control
  let extraDomainHtml = "";
  if (item.bridge_details) {
    const bd = item.bridge_details;
    extraDomainHtml = `
      <div style="background:var(--blue-light); border-left:3px solid var(--blue); padding:10px 12px; border-radius:var(--radius-sm); font-size:12px;">
        <strong style="color:var(--blue);">Bridge Managed Workspaces:</strong>
        <div style="margin-top:3px; color:var(--ink);">• Tracked GitHub: <code>${(bd.tracked_github_repos || []).join(", ") || "None"}</code></div>
        <div style="color:var(--ink);">• Safe Pull (--ff-only): <code>${(bd.pull_enabled_repos || []).join(", ") || "None"}</code></div>
        <div style="color:var(--ink);">• Cloud 1:1 Mirror: <code>${(bd.drive_profiles || []).join(", ") || "None"}</code></div>
        ${bd.last_scheduled_run ? `<div style="margin-top:4px; color:var(--blue); font-weight:600;">Last Daily Sync: ${bd.last_scheduled_run}</div>` : ""}
      </div>
    `;
  }

  if (item.model_control_details) {
    const mc = item.model_control_details;
    extraDomainHtml = `
      <div style="background:var(--amber-light); border-left:3px solid var(--amber); padding:10px 12px; border-radius:var(--radius-sm); font-size:12px;">
        <strong style="color:var(--amber);">AI Model Control Telemetry:</strong>
        <div style="margin-top:3px; color:var(--ink);">• <strong>HyperResearch</strong>: <span style="font-weight:600; color:#b45309;">[LOCKED]</span> <code>${mc.hyperresearch?.assigned_model || "muse-spark-1.3"}</code></div>
        <div style="color:var(--ink);">• <strong>PaperQA ($0)</strong>: <span style="font-weight:600; color:#047857;">[DYNAMIC FREE]</span> <code>${mc.pqa_kb?.assigned_model || "minimax-m3.1"}</code></div>
        <div style="margin-top:4px;"><a href="../model-control/index.html" target="_blank" style="color:var(--blue); font-weight:600; text-decoration:none;">Open Model Control Dashboard &nearr;</a></div>
      </div>
    `;
  }

  // Log snippet display
  let logHtml = "";
  if (item.stdout_log && item.stdout_log.exists && item.stdout_log.snippet) {
    logHtml = `
      <div>
        <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--muted); margin-bottom:4px;">
          Latest Stdout Log (${item.stdout_log.size_formatted})
        </div>
        <div class="studio-log-box">${escapeHtml(item.stdout_log.snippet)}</div>
      </div>
    `;
  } else if (item.stderr_log && item.stderr_log.exists && item.stderr_log.snippet) {
    logHtml = `
      <div>
        <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--error); margin-bottom:4px;">
          Latest Stderr Log (${item.stderr_log.size_formatted})
        </div>
        <div class="studio-log-box" style="background:#2d1413; color:#fca5a5;">${escapeHtml(item.stderr_log.snippet)}</div>
      </div>
    `;
  }

  studioCard.innerHTML = `
    <div class="studio-header">
      <div class="studio-title-group">
        <span class="studio-category">${escapeHtml(item.category)} &bull; ${escapeHtml(item.type)}</span>
        <div class="studio-name">${escapeHtml(item.name || item.label)}</div>
      </div>
      <span class="badge ${badgeClass}">${escapeHtml(item.status)}</span>
    </div>

    <!-- Quick Action Toolbar -->
    <div class="studio-actions-bar">
      <button class="primary" onclick="copyToClipboard('${escapeHtml(kickstartCmd).replace(/'/g, "\\'")}', 'Kickstart Command')">
        ${ICONS.play} Kickstart
      </button>
      ${
        reloadCmd
          ? `<button onclick="copyToClipboard('${escapeHtml(reloadCmd).replace(/'/g, "\\'")}', 'Reload Command')">
              Reload
            </button>`
          : ""
      }
      ${
        logCmd
          ? `<button onclick="copyToClipboard('${escapeHtml(logCmd).replace(/'/g, "\\'")}', 'Tail Log Command')">
              Tail Log
            </button>`
          : ""
      }
      <button onclick="copyToClipboard('${escapeHtml(item.plist_path || item.id).replace(/'/g, "\\'")}', 'Path')">
        ${ICONS.copy} Path
      </button>
    </div>

    ${extraDomainHtml}

    <!-- Metadata Matrix -->
    <div class="studio-meta-box">
      <div class="studio-meta-row">
        <span class="studio-meta-label">Schedule</span>
        <span class="studio-meta-val" style="font-weight:600;">${escapeHtml(item.schedule)}</span>
      </div>
      <div class="studio-meta-row">
        <span class="studio-meta-label">Exit Code</span>
        <span class="studio-meta-val">${item.last_exit_code ?? "-"}</span>
      </div>
      <div class="studio-meta-row">
        <span class="studio-meta-label">Plist Path</span>
        <span class="studio-meta-val" title="${escapeHtml(item.plist_path || item.id)}">${escapeHtml(item.plist_path ? item.plist_path.replace(/\/Users\/[^\/]+/, "~") : item.id)}</span>
      </div>
      <div class="studio-meta-row">
        <span class="studio-meta-label">Program</span>
        <span class="studio-meta-val" title="${escapeHtml(item.program || "")}">${escapeHtml(item.program ? item.program.replace(/\/Users\/[^\/]+/, "~") : "None")}</span>
      </div>
    </div>

    <!-- Remediation Commands Box -->
    <div class="runbook-box">
      <div class="runbook-box-title">
        ${ICONS.terminal}
        <span>Runbook Remediation Commands</span>
      </div>
      <div class="runbook-command-item">
        <span class="runbook-cmd-desc">Immediate Force Trigger:</span>
        <div class="runbook-cmd-code">
          <code>${escapeHtml(kickstartCmd)}</code>
          <button class="btn-sm" onclick="copyToClipboard('${escapeHtml(kickstartCmd).replace(/'/g, "\\'")}', 'Kickstart')">${ICONS.copy}</button>
        </div>
      </div>
      ${
        reloadCmd
          ? `<div class="runbook-command-item">
              <span class="runbook-cmd-desc">Reload Daemon Config:</span>
              <div class="runbook-cmd-code">
                <code>${escapeHtml(reloadCmd)}</code>
                <button class="btn-sm" onclick="copyToClipboard('${escapeHtml(reloadCmd).replace(/'/g, "\\'")}', 'Reload')">${ICONS.copy}</button>
              </div>
            </div>`
          : ""
      }
      ${
        lintCmd
          ? `<div class="runbook-command-item">
              <span class="runbook-cmd-desc">Validate Plist Syntax:</span>
              <div class="runbook-cmd-code">
                <code>${escapeHtml(lintCmd)}</code>
                <button class="btn-sm" onclick="copyToClipboard('${escapeHtml(lintCmd).replace(/'/g, "\\'")}', 'Lint')">${ICONS.copy}</button>
              </div>
            </div>`
          : ""
      }
    </div>

    ${logHtml}
  `;
}

function setupEventListeners() {
  // Category tabs
  document.querySelectorAll(".filter-tabs .tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-tabs .tab-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      appState.activeFilter = btn.dataset.cat;
      renderMain();
    });
  });

  // Search input
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      appState.searchQuery = e.target.value.trim();
      renderMain();
    });
  }

  // View mode switcher (List vs Cards)
  const viewListBtn = document.getElementById("viewListBtn");
  const viewCardBtn = document.getElementById("viewCardBtn");

  if (viewListBtn && viewCardBtn) {
    viewListBtn.addEventListener("click", () => {
      appState.viewMode = "list";
      viewListBtn.classList.add("active");
      viewCardBtn.classList.remove("active");
      renderMain();
    });

    viewCardBtn.addEventListener("click", () => {
      appState.viewMode = "card";
      viewCardBtn.classList.add("active");
      viewListBtn.classList.remove("active");
      renderMain();
    });
  }

  // Keyboard shortcut '/' to search
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      if (appState.isDocsView) toggleDocsView();
      if (searchInput) searchInput.focus();
    }
  });
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

document.addEventListener("DOMContentLoaded", loadData);
