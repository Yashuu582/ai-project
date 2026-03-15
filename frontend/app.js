const API = "http://localhost:8000";
let allApps = [];
let currentFilter = "All";

async function fetchApps() {
  const res = await fetch(`${API}/applications`);
  allApps = await res.json();
  renderApps();
  fetchStats();
}

async function fetchStats() {
  const res = await fetch(`${API}/stats`);
  const data = await res.json();
  document.getElementById("stat-total").textContent = `Total: ${data.total}`;
  const s = data.by_status || {};
  document.getElementById("stat-applied").textContent = `Applied: ${s.Applied || 0}`;
  document.getElementById("stat-interview").textContent = `Interview: ${s.Interview || 0}`;
  document.getElementById("stat-offer").textContent = `Offer: ${s.Offer || 0}`;
  document.getElementById("stat-rejected").textContent = `Rejected: ${s.Rejected || 0}`;
}

function renderApps() {
  const list = document.getElementById("app-list");
  const filtered = currentFilter === "All" ? allApps : allApps.filter(a => a.status === currentFilter);

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-state">No applications found.</div>`;
    return;
  }

  list.innerHTML = filtered.map(app => `
    <div class="app-card">
      <div class="app-info">
        <h3>${app.company} — ${app.role}</h3>
        <p>${new Date(app.applied_date).toLocaleDateString()} ${app.notes ? "· " + app.notes : ""}</p>
      </div>
      <div class="app-actions">
        <span class="badge badge-${app.status}">${app.status}</span>
        ${app.ai_score !== null ? `<span class="score-badge">AI: ${app.ai_score}/100</span>` : ""}
        ${(app.resume_text && app.job_description) ? `<button class="btn btn-analyze" onclick="analyzeApp(${app.id})">🧠 Analyze</button>` : ""}
        <button class="btn btn-edit" onclick="openEdit(${app.id})">✏️</button>
        <button class="btn btn-danger" onclick="deleteApp(${app.id})">🗑️</button>
      </div>
    </div>
  `).join("");
}

document.getElementById("add-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const body = {
    company: document.getElementById("company").value,
    role: document.getElementById("role").value,
    status: document.getElementById("status").value,
    job_description: document.getElementById("job_description").value || null,
    resume_text: document.getElementById("resume_text").value || null,
    notes: document.getElementById("notes").value || null,
  };
  await fetch(`${API}/applications`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  e.target.reset();
  fetchApps();
});

async function deleteApp(id) {
  if (!confirm("Delete this application?")) return;
  await fetch(`${API}/applications/${id}`, { method: "DELETE" });
  fetchApps();
}

async function analyzeApp(id) {
  const btn = event.target;
  btn.textContent = "⏳ Analyzing...";
  btn.disabled = true;
  await fetch(`${API}/applications/${id}/analyze`, { method: "POST" });
  fetchApps();
}

function openEdit(id) {
  const app = allApps.find(a => a.id === id);
  if (!app) return;
  document.getElementById("edit-id").value = app.id;
  document.getElementById("edit-company").value = app.company;
  document.getElementById("edit-role").value = app.role;
  document.getElementById("edit-status").value = app.status;
  document.getElementById("edit-jd").value = app.job_description || "";
  document.getElementById("edit-resume").value = app.resume_text || "";
  document.getElementById("edit-notes").value = app.notes || "";
  document.getElementById("modal").classList.remove("hidden");
}

async function saveEdit() {
  const id = document.getElementById("edit-id").value;
  const body = {
    company: document.getElementById("edit-company").value,
    role: document.getElementById("edit-role").value,
    status: document.getElementById("edit-status").value,
    job_description: document.getElementById("edit-jd").value || null,
    resume_text: document.getElementById("edit-resume").value || null,
    notes: document.getElementById("edit-notes").value || null,
  };
  await fetch(`${API}/applications/${id}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  closeModal();
  fetchApps();
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}

function filterApps(status, btn) {
  currentFilter = status;
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  renderApps();
}

async function quickAnalyze() {
  const resume = document.getElementById("qa-resume").value.trim();
  const jd = document.getElementById("qa-jd").value.trim();
  const resultDiv = document.getElementById("ai-result");

  if (!resume || !jd) { alert("Please provide both resume and job description."); return; }

  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = `<p class="loading">🤖 Analyzing with AI... (this may take 30-60 seconds)</p>`;

  const res = await fetch(`${API}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resume_text: resume, job_description: jd })
  });

  const data = await res.json();
  resultDiv.innerHTML = renderAIResult(data);
}

function renderAIResult(data) {
  return `
    <h3>🧠 AI Analysis Result</h3>
    <div class="score">${data.score}/100</div>
    <div class="section-title">✅ Strengths</div>
    <ul>${(data.strengths || []).map(s => `<li>${s}</li>`).join("")}</ul>
    <div class="section-title">⚠️ Gaps</div>
    <ul>${(data.gaps || []).map(g => `<li>${g}</li>`).join("")}</ul>
    <div class="section-title">💡 Suggestions</div>
    <ul>${(data.suggestions || []).map(s => `<li>${s}</li>`).join("")}</ul>
    <div class="summary">${data.summary || ""}</div>
  `;
}

fetchApps();
