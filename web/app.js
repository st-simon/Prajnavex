const statusEl = document.querySelector("#status");
const listEl = document.querySelector("#list");
const previewEl = document.querySelector("#preview");
const actionsEl = document.querySelector("#actions");

async function api(path, options) {
  const res = await fetch(path, options);
  const data = await res.json();
  if (!res.ok || data.error) throw new Error(data.error || res.statusText);
  return data;
}

async function refreshStatus() {
  const status = await api("/api/status");
  const counts = status.counts;
  statusEl.innerHTML = [
    ["Sources", counts.source || 0],
    ["Cards", counts.card || 0],
    ["Skills", counts.skill || 0],
    ["Drafts", status.drafts],
    ["Inbox Images", status.inbox_images],
    ["Errors", status.errors.length],
  ].map(([label, value]) => `<div class="metric"><strong>${value}</strong><br>${label}</div>`).join("");
}

function renderList(items, renderer) {
  listEl.innerHTML = items.map(renderer).join("") || `<div class="item">No items.</div>`;
}

async function preview(path) {
  const data = await api(`/api/file?path=${encodeURIComponent(path)}`);
  previewEl.textContent = data.text;
  actionsEl.innerHTML = "";
}

function postButton(label, path, endpoint) {
  return `<button data-post="${endpoint}" data-path="${path}">${label}</button>`;
}

async function loadInbox() {
  const data = await api("/api/inbox-images");
  renderList(data.images, item => `
    <div class="item" data-path="${item.path}" data-kind="image">
      <strong>${item.name}</strong><span>${item.path}</span>
    </div>`);
}

async function loadDrafts() {
  const data = await api("/api/drafts");
  renderList(data.drafts, item => `
    <div class="item" data-path="${item.path}" data-kind="draft">
      <strong>${item.name}</strong><span>${item.path}</span>
    </div>`);
}

async function loadIndex(type) {
  const data = await api(`/api/index?type=${type}`);
  renderList(data.records, item => `
    <div class="item" data-path="${item.path}" data-kind="note">
      <strong>${item.title || item.id}</strong><span>${item.stage || ""} · ${item.path}</span>
    </div>`);
}

async function loadView(view) {
  actionsEl.innerHTML = "";
  previewEl.textContent = "Select an item.";
  if (view === "inbox") return loadInbox();
  if (view === "drafts") return loadDrafts();
  return loadIndex(view);
}

listEl.addEventListener("click", async event => {
  const item = event.target.closest(".item");
  if (!item || !item.dataset.path) return;
  const path = item.dataset.path;
  if (item.dataset.kind === "image") {
    previewEl.textContent = path;
    actionsEl.innerHTML = postButton("Create Source Draft", path, "/api/draft-image");
    return;
  }
  await preview(path);
  if (item.dataset.kind === "draft") {
    actionsEl.innerHTML = postButton("Approve Draft", path, "/api/approve-draft");
  }
});

actionsEl.addEventListener("click", async event => {
  const button = event.target.closest("button[data-post]");
  if (!button) return;
  button.disabled = true;
  try {
    const data = await api(button.dataset.post, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({path: button.dataset.path}),
    });
    previewEl.textContent = `Done:\n${data.path}`;
    actionsEl.innerHTML = "";
    await refreshStatus();
    await loadView("drafts");
  } catch (error) {
    previewEl.textContent = error.message;
    button.disabled = false;
  }
});

document.querySelectorAll("nav button").forEach(button => {
  button.addEventListener("click", () => loadView(button.dataset.view));
});

document.querySelector("#refresh").addEventListener("click", async () => {
  await refreshStatus();
  await loadView("drafts");
});

refreshStatus().then(() => loadView("drafts"));
