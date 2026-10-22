/**
 * Bridge — Workspace & Cloud Sync Hub Controller v1.5
 * 3-Level Folder Tree View (Gitignored transparent) & Interactive Drive Sync/Exclude Toggle
 */

let state = {
  workspaces: [],
  driveProfiles: [],
  filter: 'github',       // 'github' | 'drive' | 'untracked'
  viewMode: 'list',       // 'list' | 'card'
  groupByCategory: true,
  selectedId: null,
  selectedDriveId: null,
  studioMode: 'overview', // 'overview' | 'settings'
  loading: false,
  cachedTrees: {},
  remoteDriveDirs: [],
};

// DOM Elements
const workspaceContainer = document.getElementById('workspaceContainer');
const studioCard = document.getElementById('studioCard');
const refreshBtn = document.getElementById('refreshBtn');
const liveStatus = document.getElementById('liveStatus');
const lastScanTime = document.getElementById('lastScanTime');
const totalCount = document.getElementById('totalCount');
const trackedCount = document.getElementById('trackedCount');
const driveCount = document.getElementById('driveCount');
const cleanCount = document.getElementById('cleanCount');
const pendingCount = document.getElementById('pendingCount');
const tabButtons = document.querySelectorAll('.filter-tabs .tab-btn');
const viewListBtn = document.getElementById('viewListBtn');
const viewCardBtn = document.getElementById('viewCardBtn');
const groupToggle = document.getElementById('groupToggle');

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  fetchStatus();
  fetchRemoteDriveDirs();
});

function setupEventListeners() {
  refreshBtn.addEventListener('click', () => {
    state.cachedTrees = {};
    fetchStatus();
    fetchRemoteDriveDirs();
  });

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.filter = btn.dataset.filter;
      state.studioMode = 'overview';
      renderMain();
      renderStudio();
    });
  });

  viewListBtn.addEventListener('click', () => {
    state.viewMode = 'list';
    viewListBtn.classList.add('active');
    viewCardBtn.classList.remove('active');
    renderMain();
  });

  viewCardBtn.addEventListener('click', () => {
    state.viewMode = 'card';
    viewCardBtn.classList.add('active');
    viewListBtn.classList.remove('active');
    renderMain();
  });

  groupToggle.addEventListener('change', (e) => {
    state.groupByCategory = e.target.checked;
    renderMain();
  });
}

async function fetchStatus() {
  setLoading(true);
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    if (data.success) {
      state.workspaces = data.workspaces || [];
      state.driveProfiles = data.drive_profiles || [];
      
      if (!state.selectedId || !state.workspaces.find(w => w.id === state.selectedId)) {
        state.selectedId = state.workspaces[0]?.id || null;
      }
      if (!state.selectedDriveId || !state.driveProfiles.find(p => p.id === state.selectedDriveId)) {
        state.selectedDriveId = state.driveProfiles[0]?.id || null;
      }

      updateMetrics();
      renderMain();
      renderStudio();
      updateLastScanTime();
    } else {
      showError(data.error || 'Failed to scan repositories');
    }
  } catch (err) {
    showError(err.message);
  } finally {
    setLoading(false);
  }
}

async function fetchRemoteDriveDirs() {
  try {
    const res = await fetch('/api/drive/remote_tree');
    const data = await res.json();
    if (data.success) {
      if (Array.isArray(data.directories)) {
        state.remoteDriveDirs = data.directories;
      }
      if (data.tree) {
        state.remoteDriveTree = data.tree;
      }
    }
  } catch (err) {
    console.warn('Could not fetch remote drive dirs:', err);
  }
}

async function getFolderTree(path) {
  if (!path) return null;
  if (state.cachedTrees[path]) return state.cachedTrees[path];
  try {
    const res = await fetch(`/api/workspace/tree?path=${encodeURIComponent(path)}`);
    const data = await res.json();
    if (data.success && data.tree) {
      state.cachedTrees[path] = data.tree;
      return data.tree;
    }
  } catch (err) {
    console.error('Error fetching tree:', err);
  }
  return null;
}

function setLoading(isLoading) {
  state.loading = isLoading;
  const dot = liveStatus.querySelector('.dot');
  if (isLoading) {
    dot.classList.add('loading');
    refreshBtn.disabled = true;
    lastScanTime.textContent = 'Scanning...';
  } else {
    dot.classList.remove('loading');
    refreshBtn.disabled = false;
  }
}

function updateLastScanTime() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  lastScanTime.textContent = `Live • Scanned at ${timeStr}`;
}

function updateMetrics() {
  const visibleWorkspaces = state.workspaces.filter(w => !w.is_archived);
  const total = visibleWorkspaces.length;
  const tracked = visibleWorkspaces.filter(w => w.tracked !== false).length;
  const drive = state.driveProfiles.filter(p => p.enabled !== false).length;
  const clean = visibleWorkspaces.filter(w => w.git?.status_code === 'synced').length;
  const pending = total - clean;

  totalCount.textContent = total;
  trackedCount.textContent = tracked;
  driveCount.textContent = drive;
  cleanCount.textContent = clean;
  pendingCount.textContent = pending;
}

function getAllCategories() {
  const cats = new Set();
  state.workspaces.filter(w => !w.is_archived).forEach(w => { if (w.category) cats.add(w.category); });
  state.driveProfiles.forEach(p => { if (p.category) cats.add(p.category); });
  return Array.from(cats);
}

function renderMain() {
  if (state.filter === 'drive') {
    renderDriveProfiles();
  } else {
    renderWorkspaces();
  }
}

function getFilteredWorkspaces() {
  return state.workspaces.filter(w => {
    if (w.is_archived) return false;
    const isUntracked = w.tracked === false;
    if (state.filter === 'untracked') {
      return isUntracked || !w.git?.is_git || !w.remote_repo || w.git?.status_code === 'no_remote';
    }
    if (isUntracked) return false;
    if (state.filter === 'github') return Boolean(w.remote_repo);
    return true;
  });
}

function renderWorkspaces() {
  const filtered = getFilteredWorkspaces();
  if (filtered.length === 0) {
    workspaceContainer.innerHTML = `
      <div class="loading-state">
        <p>No repositories match the current tab (<strong>${state.filter}</strong>).</p>
      </div>
    `;
    return;
  }

  if (state.groupByCategory) {
    const groups = {};
    filtered.forEach(ws => {
      const cat = ws.category || 'General';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(ws);
    });

    let html = '';
    for (const [catName, items] of Object.entries(groups)) {
      html += `
        <div class="group-section">
          <div class="group-header">
            <span>${escapeHtml(catName)}</span>
            <span>${items.length} ${items.length === 1 ? 'item' : 'items'}</span>
          </div>
          ${state.viewMode === 'list' ? renderListTable(items) : renderCardsGrid(items)}
        </div>
      `;
    }
    workspaceContainer.innerHTML = html;
  } else {
    workspaceContainer.innerHTML = state.viewMode === 'list' 
      ? renderListTable(filtered) 
      : renderCardsGrid(filtered);
  }

  attachWorkspaceEvents();
}

function renderListTable(items) {
  return `
    <div class="ws-list-table">
      ${items.map(ws => {
        const isSelected = ws.id === state.selectedId;
        const git = ws.git || {};
        const statusBadge = getStatusBadge(git, ws);
        const branchStr = ws.default_branch || git.branch || 'main';
        const displaySub = ws.remote_repo ? `github.com/${ws.remote_repo}` : (ws.path || 'Not configured');

        return `
          <div class="ws-list-row ${isSelected ? 'is-selected' : ''}" data-id="${ws.id}">
            <div>
              <span class="dot" style="width:7px;height:7px;background:${ws.tracked === false ? '#94a3b8' : (git.status_code === 'synced' ? 'var(--green)' : 'var(--amber)')}"></span>
            </div>
            
            <div class="ws-list-name-col">
              <span class="ws-list-name">${escapeHtml(ws.name)}</span>
              <span class="ws-list-sub" title="${escapeHtml(displaySub)}">${escapeHtml(displaySub)}</span>
            </div>

            <div class="ws-list-targets">
              ${ws.remote_repo ? `
                <span class="target-pill" title="GitHub: ${escapeHtml(ws.remote_repo)}">
                  <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
                  </svg>
                  ${escapeHtml(ws.remote_repo.split('/')[1] || ws.remote_repo)}
                </span>
              ` : '<span class="muted" style="font-size:11px;">No GitHub</span>'}
            </div>

            <div>
              ${statusBadge}
            </div>

            <div style="font-family:var(--font-mono);font-size:11.5px;color:var(--muted);text-align:right;">
              ⎇ ${escapeHtml(branchStr)}
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function renderCardsGrid(items) {
  return `
    <div class="ws-cards-grid">
      ${items.map(ws => {
        const isSelected = ws.id === state.selectedId;
        const git = ws.git || {};
        const statusBadge = getStatusBadge(git, ws);
        const branchStr = ws.default_branch || git.branch || 'main';
        const displaySub = ws.remote_repo ? `github.com/${ws.remote_repo}` : (ws.path || 'Not configured');

        return `
          <div class="ws-card ${isSelected ? 'is-selected' : ''}" data-id="${ws.id}">
            <div class="ws-card-header">
              <span class="ws-card-name">${escapeHtml(ws.name)}</span>
              ${statusBadge}
            </div>
            <p class="muted" style="font-size:11.5px;font-family:var(--font-mono);">${escapeHtml(displaySub)}</p>
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--muted);margin-top:auto;">
              <span>⎇ ${escapeHtml(branchStr)}</span>
              <span class="muted" style="font-size:11px;">${escapeHtml(ws.category || 'General')}</span>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

// Drive Profiles View
function renderDriveProfiles() {
  if (state.driveProfiles.length === 0) {
    workspaceContainer.innerHTML = `
      <div class="loading-state">
        <p>No Google Drive sync profiles configured.</p>
      </div>
    `;
    return;
  }

  const html = `
    <div class="ws-list-table">
      ${state.driveProfiles.map(p => {
        const isSelected = p.id === state.selectedDriveId;
        const includes = (p.include_folders || '*').split(',').map(s => s.trim()).filter(Boolean);
        const excludes = (p.exclude_patterns || '').split(',').map(s => s.trim()).filter(Boolean).slice(0, 3);

        return `
          <div class="drive-profile-row ${isSelected ? 'is-selected' : ''}" data-id="${p.id}">
            <div>
              <span class="dot" style="width:7px;height:7px;background:${p.exists ? 'var(--green)' : 'var(--amber)'}"></span>
            </div>

            <div class="ws-list-name-col">
              <span class="ws-list-name">${escapeHtml(p.name)}</span>
              <span class="ws-list-sub" title="${escapeHtml(p.source_path)}">${escapeHtml(p.source_path)}</span>
              <div class="drive-sub-tags">
                ${includes.map(inc => `<span class="drive-folder-chip">✓ ${escapeHtml(inc)}</span>`).join('')}
                ${excludes.map(exc => `<span class="drive-exclude-chip">✕ ${escapeHtml(exc)}</span>`).join('')}
              </div>
            </div>

            <div>
              <span class="target-pill" title="Destination: ${escapeHtml(p.remote_target)}">
                <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>
                </svg>
                ${escapeHtml(p.remote_target.replace('gdrive:', ''))}
              </span>
            </div>

            <div style="text-align:right;">
              <span class="badge ${p.exists ? 'badge-synced' : 'badge-dirty'}">
                ${p.exists ? 'Ready' : 'Missing'}
              </span>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;

  workspaceContainer.innerHTML = html;
  attachDriveEvents();
}

function renderStudio() {
  if (state.filter === 'drive') {
    renderDriveStudio();
  } else {
    renderWorkspaceStudio();
  }
}

// Helper to render tree nodes recursively up to depth 2 (subfolders only)
function renderTreeNodeHtml(node, depth = 0, isDrive = false, excludedSet = new Set(), parentExcluded = false) {
  if (!node || !node.is_dir) return '';
  const indent = depth * 14;

  let isExcluded = false;
  if (isDrive) {
    if (parentExcluded || excludedSet.has(node.name) || excludedSet.has(node.rel_path)) {
      isExcluded = true;
    } else {
      // Check ancestor paths (e.g. "assets/bridge" -> check "assets")
      const parts = (node.rel_path || '').split('/');
      let prefix = '';
      for (const p of parts) {
        prefix = prefix ? `${prefix}/${p}` : p;
        if (excludedSet.has(prefix)) {
          isExcluded = true;
          break;
        }
      }
    }
  }

  let rowClass = 'tree-node-row';
  if (node.is_ignored) rowClass += ' is-ignored';
  if (node.status) rowClass += ' has-change';
  if (isDrive) {
    rowClass += ' drive-interactive';
    rowClass += isExcluded ? ' drive-excluded' : ' drive-included';
  }

  const iconSvg = '📁';
  const badgeHtml = node.status ? `<span class="tree-badge ${node.status === '??' ? 'QQ' : node.status}">${node.status}</span>` : '';

  let html = `
    <div class="${rowClass}" style="padding-left:${indent + 6}px;" data-path="${escapeHtml(node.rel_path)}" data-name="${escapeHtml(node.name)}" data-isdir="true">
      <span class="tree-icon">${iconSvg}</span>
      <span class="od-truncate" title="${escapeHtml(node.name)}">${escapeHtml(node.name)}</span>
      ${badgeHtml}
    </div>
  `;

  // Maximum 2 levels of subfolders (depth 0 and depth 1)
  if (node.children && node.children.length > 0 && depth < 1) {
    node.children.forEach(child => {
      html += renderTreeNodeHtml(child, depth + 1, isDrive, excludedSet, isExcluded);
    });
  }

  return html;
}

// GitHub Workspace Studio
async function renderWorkspaceStudio() {
  const ws = state.workspaces.find(w => w.id === state.selectedId);
  if (!ws) {
    studioCard.innerHTML = `<div class="studio-empty"><p>No repository selected.</p></div>`;
    return;
  }

  const git = ws.git || {};
  const statusBadge = getStatusBadge(git, ws);
  const targetBranch = ws.default_branch || 'main';
  const availableBranches = git.available_branches && git.available_branches.length ? git.available_branches : [targetBranch];
  const allCategories = getAllCategories();

  const topNavHtml = `
    <div class="studio-top-nav">
      <div class="studio-tab-switcher">
        <button class="studio-tab-btn ${state.studioMode === 'overview' ? 'active' : ''}" id="studioTabOverview">
          Overview
        </button>
        <button class="studio-tab-btn ${state.studioMode === 'settings' ? 'active' : ''}" id="studioTabSettings">
          ⚙ Settings
        </button>
      </div>
      ${statusBadge}
    </div>
  `;

  if (state.studioMode === 'settings') {
    // Ultra-clean 4-field Settings Form (no local path, no description, no gdrive)
    studioCard.innerHTML = `
      ${topNavHtml}
      <div class="studio-header">
        <div class="studio-title-group">
          <span class="studio-category">${escapeHtml(ws.category || 'Repository')}</span>
          <h3 class="studio-name">${escapeHtml(ws.name)} Settings</h3>
        </div>
      </div>

      <form id="workspaceSettingsForm" class="settings-form">
        <!-- 1. Track in Bridge Hub -->
        <div class="form-toggle-row">
          <div>
            <strong style="display:block;font-size:12.5px;">Track in Bridge Hub</strong>
            <span class="form-hint">Monitor sync state & health across multi-repo sweeps</span>
          </div>
          <label class="switch">
            <input type="checkbox" id="inputTracked" ${ws.tracked !== false ? 'checked' : ''}>
            <span class="slider"></span>
          </label>
        </div>

        <!-- 2. Category with Quick-Chips -->
        <div class="form-group">
          <label class="form-label" for="inputCategory">Category</label>
          <input class="form-input" id="inputCategory" value="${escapeHtml(ws.category || '')}" placeholder="Type or pick an existing category">
          <div class="category-chips-list" id="categoryChips">
            ${allCategories.map(cat => `
              <button type="button" class="cat-chip" data-cat="${escapeHtml(cat)}">${escapeHtml(cat)}</button>
            `).join('')}
          </div>
        </div>

        <!-- 3. Focus Branch (Pill Selectors / Toggle) -->
        <div class="form-group">
          <label class="form-label">Focus Branch (Primary)</label>
          <div class="branch-pills-list" id="branchPills">
            ${availableBranches.map(b => `
              <button type="button" class="branch-pill ${b === targetBranch ? 'active' : ''}" data-branch="${escapeHtml(b)}">
                ● ${escapeHtml(b)}
              </button>
            `).join('')}
          </div>
          <input type="hidden" id="inputDefaultBranch" value="${escapeHtml(targetBranch)}">
          <span class="form-hint">Bridge focuses status and diffs strictly on origin/${escapeHtml(targetBranch)}</span>
        </div>

        <!-- 4. GitHub Repository -->
        <div class="form-group">
          <label class="form-label" for="inputRemoteRepo">GitHub Repository</label>
          <input class="form-input" id="inputRemoteRepo" value="${escapeHtml(ws.remote_repo || '')}" placeholder="e.g. taixuann/repo-name">
        </div>

        <!-- Buttons -->
        <div class="settings-btn-group">
          <button type="submit" class="primary" id="saveSettingsBtn">Save Changes</button>
          <button type="button" id="cancelSettingsBtn">Cancel</button>
        </div>
      </form>
    `;
    attachWorkspaceSettingsEvents(ws.id);
  } else {
    // Overview Mode with 3-Level Folder Tree
    const githubUrl = ws.remote_repo ? `https://github.com/${ws.remote_repo}` : null;
    const commit = git.last_commit;

    studioCard.innerHTML = `
      ${topNavHtml}
      <div class="studio-header">
        <div class="studio-title-group">
          <span class="studio-category">${escapeHtml(ws.category || 'Repository')}</span>
          <h3 class="studio-name">${escapeHtml(ws.name)}</h3>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="studio-actions-bar">
        ${git.exists && git.is_git ? `
          <button class="primary studio-fetch-btn" data-id="${ws.id}" title="Run git fetch">
            <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
            </svg>
            Fetch
          </button>
        ` : ''}

        ${ws.path ? `
          <button class="studio-open-btn" data-id="${ws.id}" title="Open folder in Finder">
            <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            Finder
          </button>

          <button class="studio-copy-btn" data-path="${escapeHtml(ws.path)}" title="Copy local path">
            <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
            Copy Path
          </button>
        ` : ''}
      </div>

      <!-- Metadata Box (Seamless wash) -->
      <div class="studio-meta-box">
        <div class="studio-meta-row">
          <span class="studio-meta-label">Focus Branch</span>
          <span class="studio-meta-val" style="font-weight:600;">
            ⎇ ${escapeHtml(targetBranch)}
            ${git.ahead > 0 ? `(${git.ahead} unpushed)` : ''}
            ${git.behind > 0 ? `(${git.behind} behind)` : ''}
          </span>
        </div>
        <div class="studio-meta-row">
          <span class="studio-meta-label">GitHub</span>
          ${githubUrl ? `
            <a href="${githubUrl}" target="_blank" rel="noopener" class="studio-link">
              ${escapeHtml(ws.remote_repo)} ↗
            </a>
          ` : `<span class="muted studio-meta-val">No Remote</span>`}
        </div>
        <div class="studio-meta-row">
          <span class="studio-meta-label">Local Path</span>
          <span class="studio-meta-val" title="${escapeHtml(ws.path || 'Not cloned')}">
            ${ws.path ? escapeHtml(ws.path) : '<span class="muted">Remote Only</span>'}
          </span>
        </div>
      </div>

      <!-- 2-Level Folder Tree (Gitignored transparent) -->
      <div class="studio-changes-section">
        <div class="studio-changes-header">
          <span>Folder Tree (Levels 1–2)</span>
          <span class="muted" style="font-size:11px;">Gitignored transparent</span>
        </div>
        <div class="folder-tree-box" id="workspaceTreeBox">
          <div style="padding:16px;text-align:center;color:var(--muted);font-size:12px;">
            Loading folder tree...
          </div>
        </div>
      </div>

      <!-- Latest Commit -->
      ${commit ? `
        <div class="studio-commit-box">
          <div class="commit-head">
            <span>LAST COMMIT (${escapeHtml(targetBranch)})</span>
            <span><code>${commit.hash}</code> • ${escapeHtml(commit.time)}</span>
          </div>
          <span class="commit-msg" title="${escapeHtml(commit.message)}">
            ${escapeHtml(commit.message)}
          </span>
          <span class="muted" style="font-size:11px;">by ${escapeHtml(commit.author)}</span>
        </div>
      ` : ''}
    `;

    attachOverviewEvents();

    // Populate Folder Tree asynchronously
    if (ws.path && git.exists) {
      const tree = await getFolderTree(ws.path);
      const treeBox = document.getElementById('workspaceTreeBox');
      if (treeBox) {
        if (tree && tree.children && tree.children.length > 0) {
          let treeHtml = '';
          tree.children.forEach(c => {
            treeHtml += renderTreeNodeHtml(c, 0, false);
          });
          treeBox.innerHTML = treeHtml;
        } else {
          treeBox.innerHTML = `<div class="clean-note">✓ Folder empty or clean</div>`;
        }
      }
    } else {
      const treeBox = document.getElementById('workspaceTreeBox');
      if (treeBox) treeBox.innerHTML = `<div style="padding:16px;text-align:center;color:var(--muted);font-size:12px;">Remote repository not linked to a local directory.</div>`;
    }
  }

  attachStudioNavEvents();
}

// Helper to render hierarchical Google Drive remote tree
function renderRemoteTreeNodeHtml(node, depth = 0, currentTarget = '') {
  if (!node) return '';
  const indent = depth * 14;

  const normNode = (node.path || '').replace(/\/+$/, '');
  const normTarget = (currentTarget || '').replace(/\/+$/, '');
  const isSelected = normNode === normTarget;

  let rowClass = 'remote-tree-row';
  if (isSelected) rowClass += ' is-target';

  const icon = '📁';
  const label = node.name || 'folder';

  let html = `
    <div class="${rowClass}" style="padding-left:${indent + 6}px;" data-target="${escapeHtml(node.path || '')}">
      <span class="tree-icon">${icon}</span>
      <span class="od-truncate" title="${escapeHtml(node.path || '')}">${escapeHtml(label)}</span>
      ${isSelected ? '<span class="tree-badge QQ" style="margin-left:auto;">Target</span>' : ''}
    </div>
  `;

  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      html += renderRemoteTreeNodeHtml(child, depth + 1, currentTarget);
    });
  }

  return html;
}

// Drive Studio (Granular Cloud Sync with Dual Trees: Local Upload + Remote Target)
async function renderDriveStudio() {
  const profile = state.driveProfiles.find(p => p.id === state.selectedDriveId);
  if (!profile) {
    studioCard.innerHTML = `<div class="studio-empty"><p>No Google Drive profile selected.</p></div>`;
    return;
  }

  const allCategories = getAllCategories();
  const topNavHtml = `
    <div class="studio-top-nav">
      <div class="studio-tab-switcher">
        <button class="studio-tab-btn ${state.studioMode === 'overview' ? 'active' : ''}" id="studioTabOverview">
          Overview
        </button>
        <button class="studio-tab-btn ${state.studioMode === 'settings' ? 'active' : ''}" id="studioTabSettings">
          ⚙ Settings
        </button>
      </div>
      <span class="badge ${profile.exists ? (profile.git_clean ? 'badge-synced' : 'badge-dirty') : 'badge-dirty'}">
        ${profile.exists ? (profile.git_clean ? 'Ready to Sync' : 'Commit Required') : 'Source Missing'}
      </span>
    </div>
  `;

  if (state.studioMode === 'settings') {
    // Clean Settings Form: No local source input, no exclude rules input!
    studioCard.innerHTML = `
      ${topNavHtml}
      <div class="studio-header">
        <div class="studio-title-group">
          <span class="studio-category">${escapeHtml(profile.category || 'Cloud Sync')}</span>
          <h3 class="studio-name">${escapeHtml(profile.name)} Settings</h3>
        </div>
      </div>

      <form id="driveSettingsForm" class="settings-form">
        <!-- 1. Profile Name -->
        <div class="form-group">
          <label class="form-label" for="inputDriveName">Profile Name</label>
          <input class="form-input" id="inputDriveName" value="${escapeHtml(profile.name || '')}">
        </div>

        <!-- 2. Category with Chips -->
        <div class="form-group">
          <label class="form-label" for="inputDriveCategory">Category</label>
          <input class="form-input" id="inputDriveCategory" value="${escapeHtml(profile.category || '')}">
          <div class="category-chips-list" id="driveCategoryChips">
            ${allCategories.map(cat => `
              <button type="button" class="cat-chip" data-cat="${escapeHtml(cat)}">${escapeHtml(cat)}</button>
            `).join('')}
          </div>
        </div>

        <!-- 3. Remote Destination Target -->
        <div class="form-group">
          <label class="form-label" for="inputDriveTarget">Remote Destination on Google Drive</label>
          <input class="form-input" id="inputDriveTarget" value="${escapeHtml(profile.remote_target || '')}" placeholder="gdrive:research/projects/...">
          <span class="form-hint">Tip: You can also click any directory directly on the Remote Tree on the Overview tab</span>
        </div>

        <!-- Enabled switch -->
        <div class="form-toggle-row">
          <div>
            <strong style="display:block;font-size:12.5px;">Enable Auto-Sync</strong>
            <span class="form-hint">Include in routine cloud backup jobs</span>
          </div>
          <label class="switch">
            <input type="checkbox" id="inputDriveEnabled" ${profile.enabled !== false ? 'checked' : ''}>
            <span class="slider"></span>
          </label>
        </div>

        <!-- Buttons -->
        <div class="settings-btn-group">
          <button type="submit" class="primary" id="saveDriveBtn">Save Profile</button>
          <button type="button" id="cancelDriveBtn">Cancel</button>
        </div>
      </form>
    `;
    attachDriveSettingsEvents(profile.id);
  } else {
    // Drive Overview: Pre-sync check banner, dual trees (Local Source + Remote Destination Hierarchy)
    studioCard.innerHTML = `
      ${topNavHtml}
      <div class="studio-header">
        <div class="studio-title-group">
          <span class="studio-category">${escapeHtml(profile.category || 'Cloud Sync')}</span>
          <h3 class="studio-name">${escapeHtml(profile.name)}</h3>
        </div>
      </div>

      <div class="studio-actions-bar">
        <button class="primary drive-dryrun-btn" data-id="${profile.id}">
          <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
          Check Diff (Dry Run)
        </button>

        ${profile.source_path ? `
          <button class="drive-open-btn" data-path="${escapeHtml(profile.source_path)}">
            <svg class="icon icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            Finder
          </button>
        ` : ''}
      </div>

      <!-- Pre-sync Git Status Banner -->
      ${profile.is_git ? `
        <div class="gatekeeper-banner ${profile.git_clean ? 'is-clean' : 'is-dirty'}">
          ${profile.git_clean ? '✓ Local Git is clean — Ready to Sync' : `⚠️ Git Commit Required (${profile.uncommitted_count} uncommitted changes in local repo)`}
        </div>
      ` : ''}

      <div class="studio-meta-box">
        <div class="studio-meta-row">
          <span class="studio-meta-label">Selected Drive Target</span>
          <span class="studio-meta-val" id="currentRemoteTargetBadge" style="font-weight:600;color:var(--green);">${escapeHtml(profile.remote_target)}</span>
        </div>
      </div>

      <!-- Dual Trees: Local Source (Upload Selection) + Remote Google Drive (Destination Tree) -->
      <div class="drive-dual-trees">
        <!-- 1. Local Folder Tree -->
        <div class="studio-changes-section" style="margin-top:0;">
          <div class="studio-changes-header">
            <span>Local Tree (Sync Selection)</span>
            <div class="tree-quick-actions">
              <button type="button" class="tree-action-link" id="btnSyncFull" title="Include all folders in sync">Select All</button>
              <span class="tree-action-sep">•</span>
              <button type="button" class="tree-action-link" id="btnExcludeAll" title="Exclude all folders">Clear</button>
            </div>
          </div>
          <div class="folder-tree-box" id="driveTreeBox">
            <div style="padding:16px;text-align:center;color:var(--muted);font-size:12px;">Loading local tree...</div>
          </div>
        </div>

        <!-- 2. Remote Google Drive Tree -->
        <div class="studio-changes-section" style="margin-top:0;">
          <div class="studio-changes-header">
            <span>Remote Tree (Google Drive)</span>
            <span class="muted" style="font-size:11px;">Click to set target</span>
          </div>
          <div class="remote-tree-box" id="driveRemoteTreeBox">
            <div style="padding:16px;text-align:center;color:var(--muted);font-size:12px;">Loading remote hierarchy...</div>
          </div>
        </div>
      </div>

      <div id="driveDryRunResult" style="display:none;font-family:var(--font-mono);font-size:11px;background:rgba(0,0,0,0.025);padding:12px;border-radius:var(--radius);max-height:160px;overflow-y:auto;white-space:pre-wrap;margin-top:12px;"></div>
    `;
    attachDriveOverviewEvents(profile.id);

    // Populate Local Tree asynchronously
    if (profile.source_path && profile.exists) {
      const tree = await getFolderTree(profile.source_path);
      const treeBox = document.getElementById('driveTreeBox');
      if (treeBox) {
        const rawExcludes = (profile.exclude_patterns || '').split(',').map(s => s.trim()).filter(Boolean);
        const excludedSet = new Set(rawExcludes);

        if (tree && tree.children && tree.children.length > 0) {
          let treeHtml = '';
          tree.children.forEach(c => {
            treeHtml += renderTreeNodeHtml(c, 0, true, excludedSet);
          });
          treeBox.innerHTML = treeHtml;
          attachDriveTreeToggleEvents(profile, excludedSet, tree);
          attachDriveQuickActions(profile, excludedSet, tree);
        } else {
          treeBox.innerHTML = `<div class="clean-note">✓ Source folder is empty</div>`;
        }
      }
    }

    // Populate Remote Google Drive Tree asynchronously
    const remoteBox = document.getElementById('driveRemoteTreeBox');
    if (remoteBox) {
      if (!state.remoteDriveTree) {
        await fetchRemoteDriveDirs();
      }
      if (state.remoteDriveTree && state.remoteDriveTree.children && state.remoteDriveTree.children.length > 0) {
        let remoteHtml = '';
        state.remoteDriveTree.children.forEach(c => {
          remoteHtml += renderRemoteTreeNodeHtml(c, 0, profile.remote_target);
        });
        remoteBox.innerHTML = remoteHtml;
        attachRemoteTreeEvents(profile);
      } else {
        remoteBox.innerHTML = `<div style="padding:16px;text-align:center;color:var(--muted);font-size:12px;">Unable to load Google Drive remote tree.</div>`;
      }
    }
  }

  attachStudioNavEvents();
}

function attachDriveTreeToggleEvents(profile, excludedSet, tree) {
  document.querySelectorAll('#driveTreeBox .tree-node-row.drive-interactive').forEach(row => {
    row.addEventListener('click', async (e) => {
      const name = row.dataset.name;
      const relPath = row.dataset.path;
      const targetIdentifier = relPath || name;

      if (excludedSet.has(targetIdentifier) || excludedSet.has(name)) {
        // Was excluded directly, now include it
        excludedSet.delete(targetIdentifier);
        excludedSet.delete(name);
      } else {
        // Was included, now exclude it
        excludedSet.add(targetIdentifier);
      }

      // Re-render folder tree immediately so all child folders visually inherit exclusion/inclusion state
      const treeBox = document.getElementById('driveTreeBox');
      if (treeBox && tree && tree.children) {
        let treeHtml = '';
        tree.children.forEach(c => {
          treeHtml += renderTreeNodeHtml(c, 0, true, excludedSet);
        });
        treeBox.innerHTML = treeHtml;
        attachDriveTreeToggleEvents(profile, excludedSet, tree);
      }

      // Auto-save updated exclude patterns
      const newExcludesStr = Array.from(excludedSet).join(', ');
      profile.exclude_patterns = newExcludesStr;

      try {
        await fetch('/api/drive/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: profile.id,
            updates: { exclude_patterns: newExcludesStr },
          }),
        });
      } catch (err) {
        console.error('Failed to auto-save exclude rules:', err);
      }
    });
  });
}

function attachDriveQuickActions(profile, excludedSet, tree) {
  const syncFullBtn = document.getElementById('btnSyncFull');
  const excludeAllBtn = document.getElementById('btnExcludeAll');

  if (syncFullBtn) {
    syncFullBtn.addEventListener('click', async () => {
      excludedSet.clear();
      profile.exclude_patterns = '';

      const treeBox = document.getElementById('driveTreeBox');
      if (treeBox && tree && tree.children) {
        let treeHtml = '';
        tree.children.forEach(c => {
          treeHtml += renderTreeNodeHtml(c, 0, true, excludedSet);
        });
        treeBox.innerHTML = treeHtml;
        attachDriveTreeToggleEvents(profile, excludedSet, tree);
      }

      try {
        await fetch('/api/drive/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: profile.id,
            updates: { exclude_patterns: '' },
          }),
        });
      } catch (err) {
        console.error('Failed to save full sync selection:', err);
      }
    });
  }

  if (excludeAllBtn) {
    excludeAllBtn.addEventListener('click', async () => {
      if (tree && tree.children) {
        tree.children.forEach(c => {
          excludedSet.add(c.name);
          if (c.rel_path) excludedSet.add(c.rel_path);
        });
      }
      const newExcludesStr = Array.from(excludedSet).join(', ');
      profile.exclude_patterns = newExcludesStr;

      const treeBox = document.getElementById('driveTreeBox');
      if (treeBox && tree && tree.children) {
        let treeHtml = '';
        tree.children.forEach(c => {
          treeHtml += renderTreeNodeHtml(c, 0, true, excludedSet);
        });
        treeBox.innerHTML = treeHtml;
        attachDriveTreeToggleEvents(profile, excludedSet, tree);
      }

      try {
        await fetch('/api/drive/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: profile.id,
            updates: { exclude_patterns: newExcludesStr },
          }),
        });
      } catch (err) {
        console.error('Failed to save exclude all selection:', err);
      }
    });
  }
}

function attachRemoteTreeEvents(profile) {
  document.querySelectorAll('#driveRemoteTreeBox .remote-tree-row').forEach(row => {
    row.addEventListener('click', async () => {
      const target = row.dataset.target;
      if (!target) return;
      profile.remote_target = target;

      const targetBadge = document.getElementById('currentRemoteTargetBadge');
      if (targetBadge) targetBadge.textContent = target;

      // Re-render remote tree to highlight newly selected target
      const remoteBox = document.getElementById('driveRemoteTreeBox');
      if (remoteBox && state.remoteDriveTree && state.remoteDriveTree.children) {
        let remoteHtml = '';
        state.remoteDriveTree.children.forEach(c => {
          remoteHtml += renderRemoteTreeNodeHtml(c, 0, target);
        });
        remoteBox.innerHTML = remoteHtml;
        attachRemoteTreeEvents(profile);
      }

      // Auto-save remote_target to backend
      try {
        await fetch('/api/drive/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: profile.id,
            updates: { remote_target: target },
          }),
        });
      } catch (err) {
        console.error('Failed to auto-save remote target:', err);
      }
    });
  });
}

function attachWorkspaceEvents() {
  document.querySelectorAll('.ws-list-row, .ws-card').forEach(el => {
    el.addEventListener('click', () => {
      state.selectedId = el.dataset.id;
      state.studioMode = 'overview';
      renderWorkspaces();
      renderStudio();
    });
  });
}

function attachDriveEvents() {
  document.querySelectorAll('.drive-profile-row').forEach(el => {
    el.addEventListener('click', () => {
      state.selectedDriveId = el.dataset.id;
      state.studioMode = 'overview';
      renderDriveProfiles();
      renderStudio();
    });
  });
}

function attachStudioNavEvents() {
  const tabOverview = studioCard.querySelector('#studioTabOverview');
  const tabSettings = studioCard.querySelector('#studioTabSettings');
  const configBtn = studioCard.querySelector('.studio-config-btn');

  if (tabOverview) {
    tabOverview.addEventListener('click', () => {
      state.studioMode = 'overview';
      renderStudio();
    });
  }
  if (tabSettings) {
    tabSettings.addEventListener('click', () => {
      state.studioMode = 'settings';
      renderStudio();
    });
  }
  if (configBtn) {
    configBtn.addEventListener('click', () => {
      state.studioMode = 'settings';
      renderStudio();
    });
  }
}

function attachOverviewEvents() {
  const fetchBtn = studioCard.querySelector('.studio-fetch-btn');
  if (fetchBtn) {
    fetchBtn.addEventListener('click', async () => {
      const id = fetchBtn.dataset.id;
      fetchBtn.disabled = true;
      fetchBtn.innerHTML = `Fetching...`;
      try {
        const res = await fetch('/api/workspace/fetch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id }),
        });
        const data = await res.json();
        if (data.success) {
          state.cachedTrees = {};
          await fetchStatus();
        } else {
          alert('Fetch error: ' + (data.error || 'Failed'));
        }
      } catch (err) {
        alert('Network error: ' + err.message);
      } finally {
        fetchBtn.disabled = false;
        fetchBtn.innerHTML = `Fetch`;
      }
    });
  }

  const openBtn = studioCard.querySelector('.studio-open-btn');
  if (openBtn) {
    openBtn.addEventListener('click', async () => {
      const id = openBtn.dataset.id;
      try {
        await fetch('/api/workspace/open', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id }),
        });
      } catch (err) {
        console.error('Open error:', err);
      }
    });
  }

  const copyBtn = studioCard.querySelector('.studio-copy-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const p = copyBtn.dataset.path;
      navigator.clipboard.writeText(p).then(() => {
        copyBtn.innerHTML = `✓ Copied!`;
        setTimeout(() => { copyBtn.innerHTML = `Copy Path`; }, 1500);
      });
    });
  }
}

function attachWorkspaceSettingsEvents(workspaceId) {
  const form = document.getElementById('workspaceSettingsForm');
  const cancelBtn = document.getElementById('cancelSettingsBtn');
  const catInput = document.getElementById('inputCategory');
  const branchInput = document.getElementById('inputDefaultBranch');

  document.querySelectorAll('#categoryChips .cat-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if (catInput) catInput.value = chip.dataset.cat;
    });
  });

  document.querySelectorAll('#branchPills .branch-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      document.querySelectorAll('#branchPills .branch-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      if (branchInput) branchInput.value = pill.dataset.branch;
    });
  });

  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      state.studioMode = 'overview';
      renderStudio();
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const saveBtn = document.getElementById('saveSettingsBtn');
      saveBtn.disabled = true;
      saveBtn.innerHTML = 'Saving...';

      const tracked = document.getElementById('inputTracked').checked;
      const category = catInput.value.trim() || 'General';
      const default_branch = branchInput.value.trim() || 'main';
      const remote_repo = document.getElementById('inputRemoteRepo').value.trim() || null;

      try {
        const res = await fetch('/api/workspace/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: workspaceId,
            updates: { tracked, category, default_branch, remote_repo },
          }),
        });
        const data = await res.json();
        if (data.success) {
          state.workspaces = data.workspaces || [];
          state.studioMode = 'overview';
          updateMetrics();
          renderMain();
          renderStudio();
        } else {
          alert('Save error: ' + (data.error || 'Failed'));
        }
      } catch (err) {
        alert('Network error: ' + err.message);
      } finally {
        saveBtn.disabled = false;
        saveBtn.innerHTML = 'Save Changes';
      }
    });
  }
}

function attachDriveSettingsEvents(profileId) {
  const form = document.getElementById('driveSettingsForm');
  const cancelBtn = document.getElementById('cancelDriveBtn');
  const catInput = document.getElementById('inputDriveCategory');
  const targetInput = document.getElementById('inputDriveTarget');

  document.querySelectorAll('#driveCategoryChips .cat-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if (catInput) catInput.value = chip.dataset.cat;
    });
  });

  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      state.studioMode = 'overview';
      renderStudio();
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const saveBtn = document.getElementById('saveDriveBtn');
      saveBtn.disabled = true;
      saveBtn.innerHTML = 'Saving...';

      const name = document.getElementById('inputDriveName').value.trim();
      const category = catInput ? catInput.value.trim() : 'Cloud Sync';
      const remote_target = targetInput ? targetInput.value.trim() : '';
      const enabled = document.getElementById('inputDriveEnabled').checked;

      try {
        const res = await fetch('/api/drive/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: profileId,
            updates: { name, category, remote_target, enabled },
          }),
        });
        const data = await res.json();
        if (data.success) {
          state.driveProfiles = data.drive_profiles || [];
          state.studioMode = 'overview';
          updateMetrics();
          renderMain();
          renderStudio();
        } else {
          alert('Save error: ' + (data.error || 'Failed'));
        }
      } catch (err) {
        alert('Network error: ' + err.message);
      } finally {
        saveBtn.disabled = false;
        saveBtn.innerHTML = 'Save Profile';
      }
    });
  }
}

function attachDriveOverviewEvents(profileId) {
  const dryRunBtn = studioCard.querySelector('.drive-dryrun-btn');
  const openBtn = studioCard.querySelector('.drive-open-btn');
  const resultBox = document.getElementById('driveDryRunResult');

  if (openBtn) {
    openBtn.addEventListener('click', async () => {
      const p = openBtn.dataset.path;
      try {
        await fetch('/api/workspace/open', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: profileId }),
        });
      } catch (err) {
        console.error('Error opening folder:', err);
      }
    });
  }

  if (dryRunBtn) {
    dryRunBtn.addEventListener('click', async () => {
      dryRunBtn.disabled = true;
      dryRunBtn.innerHTML = 'Checking...';
      resultBox.style.display = 'block';
      resultBox.textContent = 'Running rclone check --dry-run...';

      try {
        const res = await fetch('/api/drive/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: profileId }),
        });
        const data = await res.json();
        if (data.success) {
          resultBox.textContent = data.output || 'Check passed with 0 errors.';
        } else {
          resultBox.textContent = 'Check failed: ' + (data.error || 'Error');
        }
      } catch (err) {
        resultBox.textContent = 'Error: ' + err.message;
      } finally {
        dryRunBtn.disabled = false;
        dryRunBtn.innerHTML = 'Check Diff (Dry Run)';
      }
    });
  }
}

function getStatusBadge(git, ws) {
  if (ws && ws.tracked === false) {
    return `<span class="badge badge-no-remote">Untracked</span>`;
  }
  if (!ws.path || !git.exists) {
    return `<span class="badge badge-no-remote">Remote Only</span>`;
  }
  if (!git.is_git || git.status_code === 'no_git') {
    return `<span class="badge badge-no-remote">No Git</span>`;
  }
  if (git.status_code === 'no_remote') {
    return `<span class="badge badge-no-remote">No Remote</span>`;
  }
  if (git.status_code === 'dirty') {
    return `<span class="badge badge-dirty">● ${escapeHtml(git.status_label)}</span>`;
  }
  if (git.status_code === 'ahead') {
    return `<span class="badge badge-ahead">▲ ${escapeHtml(git.status_label)}</span>`;
  }
  if (git.status_code === 'behind') {
    return `<span class="badge badge-behind">▼ ${escapeHtml(git.status_label)}</span>`;
  }
  if (git.status_code === 'synced') {
    return `<span class="badge badge-synced">✓ In Sync</span>`;
  }
  return `<span class="badge badge-no-remote">${escapeHtml(git.status_label || 'Unknown')}</span>`;
}

function showError(msg) {
  workspaceContainer.innerHTML = `
    <div class="loading-state">
      <p style="color:var(--error);font-weight:600;">Error: ${escapeHtml(msg)}</p>
      <button class="primary" onclick="fetchStatus()">Retry</button>
    </div>
  `;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
