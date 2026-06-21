const SIGNAL_STATUS = Object.freeze({
  OPEN: "Open",
  NEEDS_VALIDATION: "Needs validation",
  CLOSED: "Closed",
  DEFERRED: "Deferred",
});

const SIGNAL_SEVERITY = Object.freeze({
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
});

const EVIDENCE_ARTIFACTS = Object.freeze({
  scanReport: {
    reportMd: "docs/security-scans/FCCSecurity/no-head_20260618T085508-0300/report.md",
    reportHtml: "docs/security-scans/FCCSecurity/no-head_20260618T085508-0300/report.html",
  },
  zip: "output/fccsecurity-frontier-cyber-intelligence.zip",
  zipSha256: "output/fccsecurity-frontier-cyber-intelligence.zip.sha256",
});

const DEPLOY_STATE = Object.freeze({
  repository: "https://github.com/aisamuraiagent-source/FCCSecurity-Public",
  visibility: "public",
  publicUrls: {
    githubPages: "https://aisamuraiagent-source.github.io/FCCSecurity-Public/",
    netlify: null,
    other: []
  },
  gate: {
    status: "validated",
    reason: "Public publication state reconciled to match repository/public page reality.",
    dominantRisk: "none"
  }
});

const signals = [
  {
    id: "SIG-001",
    title: "Public claim drift in security evidence",
    summary: "Documentation was reconciled against local validation and Codex Security receipts.",
    severity: SIGNAL_SEVERITY.MEDIUM,
    status: SIGNAL_STATUS.CLOSED,
    source: "docs/evidence",
    owner: "Codex",
    category: "closed",
    evidence: "README, VERSION, validation docs, and scan report now agree on completed local validation.",
    action: "Keep future public wording tied to fresh validation receipts before publication."
  },
  {
    id: "SIG-002",
    title: "Runtime rendering sink control",
    summary: "Dynamic UI rendering preserves text-only writes for operator notes and signal labels.",
    severity: SIGNAL_SEVERITY.HIGH,
    status: SIGNAL_STATUS.CLOSED,
    source: "app.js",
    owner: "FCC Security",
    category: "closed",
    evidence: "Codex Security scan and sink grep found no runtime unsafe DOM or dynamic execution sinks.",
    action: "Keep data rendering on textContent/createElement and re-run sink checks."
  },
  {
    id: "SIG-003",
    title: "Codex Security repository scan completed",
    summary: "Repo-wide Codex Security scan covered runtime, docs, deployment evidence, and threat model surfaces.",
    severity: SIGNAL_SEVERITY.LOW,
    status: SIGNAL_STATUS.CLOSED,
    source: "Codex Security skill",
    owner: "Codex",
    category: "closed",
    evidence: `Final reports written to ${EVIDENCE_ARTIFACTS.scanReport.reportMd} and ${EVIDENCE_ARTIFACTS.scanReport.reportHtml}.`,
    action: "Use report.md/report.html as release-gate evidence before external deployment."
  },
  {
    id: "SIG-004",
    title: "Local-only intelligence state",
    summary: "Operator notes and selected signal state stay in the browser through localStorage.",
    severity: SIGNAL_SEVERITY.LOW,
    status: SIGNAL_STATUS.CLOSED,
    source: "browser localStorage",
    owner: "FCC Security",
    category: "closed",
    evidence: "No backend or network path exists in the current prototype.",
    action: "Keep local state bounded; avoid storing secrets or personal identifiers."
  },
  {
    id: "SIG-005",
    title: "Public release state reconciled with actual repository state",
    summary: `Repository visibility is ${DEPLOY_STATE.visibility} and GitHub Pages is public at ${DEPLOY_STATE.publicUrls.githubPages}.`,
    severity: SIGNAL_SEVERITY.LOW,
    status: SIGNAL_STATUS.CLOSED,
    source: "app.js / DEPLOY_STATE",
    owner: "FCC Security",
    category: "closed",
    evidence: `Repository: ${DEPLOY_STATE.repository}; public URL: ${DEPLOY_STATE.publicUrls.githubPages}; gate status: ${DEPLOY_STATE.gate.status}.`,
    action: "Keep release status synchronized with actual repository visibility and public URL in both README and timeline."
  }
];

const threatSurfaces = [
  {
    name: "Public evidence credibility",
    detail: "README, validation docs, scan outputs, and portfolio wording must not overclaim."
  },
  {
    name: "Local operator state",
    detail: "Notes and selections are browser-local and must not become a secret store."
  },
  {
    name: "Rendering boundary",
    detail: "Signal data is untrusted by default and must render through text-safe APIs."
  },
  {
    name: "Scan workflow integrity",
    detail: "Coverage, validation, and attack-path receipts must stay explicit and auditable."
  }
];

const ledgerRows = [
  ["Static UI runtime", "not_applicable", "No backend, no auth, no external API"],
  ["DOM rendering", "suppressed", "No unsafe runtime sink found in reviewed files"],
  ["Public claims", "closed", "All public claims now match repository URL visibility and scan evidence."],
  ["Local storage", "suppressed", "No secrets intended; warning documented"]
];

const timeline = [
  ["2026-06-16 09:54", "UI concept generated for operational dashboard direction."],
  ["2026-06-16 10:00", "Repository scaffold created as static local-first prototype."],
  ["2026-06-16 10:05", "Threat model persisted for future Codex Security workflow."],
  ["2026-06-18 08:55", "Repo-wide Codex Security scan completed (no-head_20260618T085508-0300) with zero surviving reportable findings."],
  ["2026-06-21 10:00", "Release gate state formalized and reconciled for public visibility against GitHub Pages."],
  ["2026-06-21 16:00", "Repository and app state updated to public deploy state: https://aisamuraiagent-source.github.io/FCCSecurity-Public/."]
];

const state = {
  filter: "all",
  selectedId: localStorage.getItem("fcc:selectedSignal") || signals[0].id
};

const elements = {
  riskScore: document.querySelector("#riskScore"),
  riskTrend: document.querySelector("#riskTrend"),
  openSignals: document.querySelector("#openSignals"),
  validatedSignals: document.querySelector("#validatedSignals"),
  deferredSignals: document.querySelector("#deferredSignals"),
  threatList: document.querySelector("#threatList"),
  signalList: document.querySelector("#signalList"),
  queueTitle: document.querySelector("#queueTitle"),
  detailTitle: document.querySelector("#detailTitle"),
  detailSeverity: document.querySelector("#detailSeverity"),
  detailSummary: document.querySelector("#detailSummary"),
  detailSource: document.querySelector("#detailSource"),
  detailStatus: document.querySelector("#detailStatus"),
  detailOwner: document.querySelector("#detailOwner"),
  operatorNotes: document.querySelector("#operatorNotes"),
  ledgerRows: document.querySelector("#ledgerRows"),
  timelineList: document.querySelector("#timelineList"),
  exportSnapshot: document.querySelector("#exportSnapshot"),
  markReviewed: document.querySelector("#markReviewed"),
  escalateSignal: document.querySelector("#escalateSignal")
};

function createTextElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  element.textContent = text;
  return element;
}

function clearNode(node) {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}

function severityClass(severity) {
  return severity.toLowerCase();
}

function filteredSignals() {
  if (state.filter === "all") {
    return signals;
  }

  if (state.filter === "high") {
    return signals.filter((signal) => signal.severity === SIGNAL_SEVERITY.HIGH);
  }

  if (state.filter === "validation") {
    return signals.filter((signal) => signal.status === SIGNAL_STATUS.NEEDS_VALIDATION || signal.status === SIGNAL_STATUS.OPEN);
  }

  return signals.filter((signal) => signal.status === SIGNAL_STATUS.CLOSED || signal.status === SIGNAL_STATUS.DEFERRED);
}

function selectedSignal() {
  return signals.find((signal) => signal.id === state.selectedId) || signals[0];
}

function renderMetrics() {
  const open = signals.filter((signal) => signal.status === "Open" || signal.status === "Needs validation").length;
  const validated = signals.filter((signal) => signal.status === "Closed").length;
  const deferred = signals.filter((signal) => signal.status === "Deferred").length;
  const score = Math.round((open * 28 + deferred * 10 + validated * 4) / signals.length);

  elements.riskScore.textContent = String(score);
  elements.riskTrend.textContent = open > 1 ? "review" : "stable";
  elements.openSignals.textContent = String(open);
  elements.validatedSignals.textContent = String(validated);
  elements.deferredSignals.textContent = String(deferred);
}

function renderThreatModel() {
  clearNode(elements.threatList);
  threatSurfaces.forEach((surface) => {
    const item = document.createElement("li");
    item.className = "threat-item";
    item.append(
      createTextElement("strong", "", surface.name),
      createTextElement("span", "", surface.detail)
    );
    elements.threatList.appendChild(item);
  });
}

function renderSignals() {
  const list = filteredSignals();
  const title = {
    all: "All signals",
    high: "High impact",
    validation: "Needs validation",
    closed: "Closed or deferred"
  }[state.filter];

  elements.queueTitle.textContent = title;
  clearNode(elements.signalList);

  list.forEach((signal) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = signal.id === state.selectedId ? "signal-card active" : "signal-card";
    card.dataset.signalId = signal.id;

    const topLine = document.createElement("div");
    topLine.className = "signal-topline";
    topLine.append(
      createTextElement("p", "signal-title", signal.title),
      createTextElement("span", `status-badge ${severityClass(signal.severity)}`, signal.severity)
    );

    const meta = document.createElement("div");
    meta.className = "signal-meta";
    meta.append(
      createTextElement("span", "status-badge", signal.id),
      createTextElement("span", "status-badge", signal.status)
    );

    card.append(
      topLine,
      createTextElement("p", "signal-summary", signal.summary),
      meta
    );

    card.addEventListener("click", () => {
      state.selectedId = signal.id;
      localStorage.setItem("fcc:selectedSignal", state.selectedId);
      renderAll();
    });

    elements.signalList.appendChild(card);
  });
}

function renderDetail() {
  const signal = selectedSignal();
  const savedNotes = localStorage.getItem(`fcc:notes:${signal.id}`) || "";

  elements.detailTitle.textContent = signal.title;
  elements.detailSeverity.textContent = signal.severity;
  elements.detailSeverity.className = `severity-badge ${severityClass(signal.severity)}`;
  elements.detailSummary.textContent = `${signal.summary} Next action: ${signal.action}`;
  elements.detailSource.textContent = signal.source;
  elements.detailStatus.textContent = signal.status;
  elements.detailOwner.textContent = signal.owner;
  elements.operatorNotes.value = savedNotes;
}

function renderLedger() {
  clearNode(elements.ledgerRows);
  ledgerRows.forEach(([surface, disposition, evidence]) => {
    const row = document.createElement("div");
    row.className = "ledger-row";
    row.setAttribute("role", "row");
    row.append(
      createTextElement("span", "", surface),
      createTextElement("span", "", disposition),
      createTextElement("span", "", evidence)
    );
    elements.ledgerRows.appendChild(row);
  });
}

function renderTimeline() {
  clearNode(elements.timelineList);
  timeline.forEach(([time, receipt]) => {
    const item = document.createElement("li");
    item.className = "timeline-item";
    item.append(
      createTextElement("strong", "", time),
      createTextElement("span", "", receipt)
    );
    elements.timelineList.appendChild(item);
  });
}

function renderAll() {
  renderMetrics();
  renderThreatModel();
  renderSignals();
  renderDetail();
  renderLedger();
  renderTimeline();
}

function setFilter(filter) {
  state.filter = filter;
  document.querySelectorAll(".filter-chip").forEach((button) => {
    button.classList.toggle("active", button.dataset.filter === filter);
  });
  renderSignals();
}

function exportSnapshot() {
  const signal = selectedSignal();
  const snapshot = {
    generatedAt: new Date().toISOString(),
    selectedSignal: signal,
    notes: elements.operatorNotes.value,
    metrics: {
      open: elements.openSignals.textContent,
      validated: elements.validatedSignals.textContent,
      deferred: elements.deferredSignals.textContent,
      score: elements.riskScore.textContent
    }
  };
  const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "fcc-security-snapshot.json";
  link.click();
  URL.revokeObjectURL(link.href);
}

document.querySelectorAll(".filter-chip").forEach((button) => {
  button.addEventListener("click", () => setFilter(button.dataset.filter));
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

elements.operatorNotes.addEventListener("input", () => {
  localStorage.setItem(`fcc:notes:${selectedSignal().id}`, elements.operatorNotes.value);
});

elements.markReviewed.addEventListener("click", () => {
  const signal = selectedSignal();
  signal.status = "Closed";
  renderAll();
});

elements.escalateSignal.addEventListener("click", () => {
  const signal = selectedSignal();
  signal.status = "Needs validation";
  signal.severity = signal.severity === "low" ? "medium" : signal.severity;
  renderAll();
});

elements.exportSnapshot.addEventListener("click", exportSnapshot);

renderAll();
