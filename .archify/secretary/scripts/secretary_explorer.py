#!/usr/bin/env python3
"""Build the Secretary unified profile explorer.

Reads docs/profiles/secretary/capabilities.yaml and an authored workflow mapping,
validates every mapped capability ID against the YAML, then derives the final
self-contained HTML by injecting preview controls into the finalized native
Archify baseline document. Switches are preview only and are never persisted.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(HERE))
import profile_capabilities as pc

REPO_ROOT = pc.REPO_ROOT
PROFILE = "secretary"
GROUPS = ("skills", "plugins", "mcps", "external_tools", "automation")
GROUP_LABELS = {
    "skills": "Skills",
    "plugins": "Plugins",
    "mcps": "MCPs",
    "external_tools": "External tools",
    "automation": "Automation",
}

KNOWN_STAGE_IDS = {
    "request",
    "inspect",
    "memory_context",
    "brainstorm",
    "plan",
    "perform_direct",
    "delegate",
    "skill_work",
    "verify",
    "record_report",
    "render_map",
}


class MappingError(ValueError):
    pass


def capability_ids_from_yaml(data: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for section in GROUPS:
        for item in data.get(section, []):
            if isinstance(item, str):
                ids.add(item)
            elif isinstance(item, dict):
                ids.add(item["name"])
    return ids


def load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = pc.load_yaml_text(text)
    except (pc.DuplicateKeyError, yaml.YAMLError, ValueError) as exc:
        raise MappingError(f"invalid workflow mapping YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise MappingError("workflow mapping must be a mapping")
    if "stages" not in data or not isinstance(data["stages"], list):
        raise MappingError("workflow mapping must contain a 'stages' list")
    return data


def validate_mapping(mapping: dict[str, Any], valid_ids: set[str]) -> None:
    if not isinstance(mapping, dict):
        raise MappingError("workflow mapping must be a mapping")
    if "stages" not in mapping or not isinstance(mapping["stages"], list):
        raise MappingError("workflow mapping must contain a 'stages' list")
    if not mapping["stages"]:
        raise MappingError("workflow mapping stages must not be empty")
    seen_stage_ids: set[str] = set()
    for stage in mapping["stages"]:
        if not isinstance(stage, dict):
            raise MappingError("each stage must be a mapping")
        for key in ("id", "label"):
            if key not in stage or not isinstance(stage[key], str) or not stage[key].strip():
                raise MappingError(f"stage missing string {key!r}")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", stage["id"]):
            raise MappingError(f"invalid stage id: {stage['id']!r}")
        if stage["id"] in seen_stage_ids:
            raise MappingError(f"duplicate stage id: {stage['id']!r}")
        seen_stage_ids.add(stage["id"])
        cap_ids = stage.get("capability_ids", [])
        if not isinstance(cap_ids, list) or not all(isinstance(x, str) for x in cap_ids):
            raise MappingError(f"stage {stage['id']!r} capability_ids must be a list of strings")
        if len(set(cap_ids)) != len(cap_ids):
            raise MappingError(f"stage {stage['id']!r} has duplicate capability_ids")
        unknown = [cap_id for cap_id in cap_ids if cap_id not in valid_ids]
        if unknown:
            raise MappingError(
                "workflow mapping references unknown capability id(s): "
                + ", ".join(repr(x) for x in unknown)
            )
        allowed = {"id", "label", "capability_ids"}
        extra = set(stage) - allowed
        if extra:
            raise MappingError(f"stage {stage['id']!r} has unexpected key(s): {sorted(extra)}")


def yaml_path(repo_root: Path) -> Path:
    return repo_root / "docs" / "profiles" / PROFILE / "capabilities.yaml"


def mapping_path(repo_root: Path) -> Path:
    return repo_root / "automation" / "profile-capabilities" / "workflow-mapping.yaml"


def output_path(repo_root: Path) -> Path:
    return repo_root / ".archify" / "secretary" / "native" / "profile-legacy.html"


def baseline_path(repo_root: Path) -> Path:
    return repo_root / ".archify" / "secretary" / "native" / "unified-baseline.html"


def group_entries(data: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for group in GROUPS:
        result[group] = [pc.entry_text(item) for item in data.get(group, [])]
    return result


def capability_node_id(cap_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "_", cap_id).strip("_").lower()
    if not safe:
        safe = "capability"
    return f"cap_{safe}"


def capability_nodes(data: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for group in GROUPS:
        for item in data.get(group, []):
            cid = item if isinstance(item, str) else item["name"]
            result[cid] = capability_node_id(cid)
    return result


def make_model(data: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    valid_ids = capability_ids_from_yaml(data)
    validate_mapping(mapping, valid_ids)
    for stage in mapping["stages"]:
        if stage["id"] not in KNOWN_STAGE_IDS:
            raise MappingError(f"unknown graph stage id: {stage['id']!r}")
    stage_ids = {s["id"] for s in mapping["stages"]}
    connections: list[dict[str, str]] = []
    connections.append({"from": "identity", "to": "inspect"})
    connections.append({"from": "permissions", "to": "delegate"})
    workflow_edges = [
        ("request", "inspect"),
        ("inspect", "memory_context"),
        ("inspect", "brainstorm"),
        ("inspect", "plan"),
        ("inspect", "perform_direct"),
        ("brainstorm", "plan"),
        ("plan", "delegate"),
        ("perform_direct", "verify"),
        ("delegate", "verify"),
        ("verify", "record_report"),
    ]
    for a, b in workflow_edges:
        if a in stage_ids and b in stage_ids:
            connections.append({"from": a, "to": b})
    for stage in mapping["stages"]:
        for cap_id in stage.get("capability_ids", []):
            connections.append({"from": capability_node_id(cap_id), "to": stage["id"]})
    return {"connections": connections, "stages": [s["id"] for s in mapping["stages"]]}


def controls_html(data: dict[str, Any], mapping: dict[str, Any]) -> str:
    valid_ids = capability_ids_from_yaml(data)
    stages_by_cap: dict[str, list[str]] = {cap: [] for cap in valid_ids}
    stage_labels: dict[str, str] = {}
    for stage in mapping["stages"]:
        stage_labels[stage["id"]] = stage["label"]
        for cap_id in stage.get("capability_ids", []):
            stages_by_cap.setdefault(cap_id, []).append(stage["id"])
    parts: list[str] = []
    for group in GROUPS:
        for item in data.get(group, []):
            cid = item if isinstance(item, str) else item["name"]
            stages = stages_by_cap.get(cid, [])
            if stages:
                stages_text = ", ".join(html.escape(stage_labels.get(s, s)) for s in stages)
            else:
                stages_text = "Not assessed: no authored stage dependency"
            detail = ""
            if isinstance(item, dict):
                extras = [item[k] for k in ("detail", "note", "description") if item.get(k)]
                detail = "; ".join(extras)
            parts.append(
                f'<div class="control-row">{html.escape(cid)} - {stages_text}'
                + (f' ({html.escape(detail)})' if detail else "")
                + "</div>"
            )
    for stage in mapping["stages"]:
        parts.append(f'<span class="stage-label">{html.escape(stage["label"])}</span>')
    return "".join(parts)


def _controls_markup(data: dict[str, Any], mapping: dict[str, Any]) -> str:
    valid_ids = capability_ids_from_yaml(data)
    stages_by_cap: dict[str, list[str]] = {cap: [] for cap in valid_ids}
    stage_labels: dict[str, str] = {}
    stage_caps: dict[str, list[str]] = {}
    for stage in mapping["stages"]:
        stage_labels[stage["id"]] = stage["label"]
        stage_caps[stage["id"]] = list(stage.get("capability_ids", []))
        for cap_id in stage.get("capability_ids", []):
            stages_by_cap.setdefault(cap_id, []).append(stage["id"])

    cap_detail: dict[str, str] = {}
    for group in GROUPS:
        for item in data.get(group, []):
            if isinstance(item, dict):
                cid = item["name"]
                extras = [item[k] for k in ("detail", "note", "description") if item.get(k)]
                cap_detail[cid] = "; ".join(extras)

    all_caps = []
    for group in GROUPS:
        for item in data.get(group, []):
            cid = item if isinstance(item, str) else item["name"]
            all_caps.append(cid)

    cap_sections_html = []
    for group in GROUPS:
        entries = [(item if isinstance(item, str) else item["name"]) for item in data.get(group, [])]
        items_html = []
        if not entries:
            items_html.append('<li class="empty-category">None approved</li>')
        for cid in entries:
            stages = stages_by_cap.get(cid, [])
            stage_attr = html.escape(json.dumps(stages))
            detail = cap_detail.get(cid, "")
            detail_html = f'<span class="cap-detail">{html.escape(detail)}</span>' if detail else ""
            stages_text = ", ".join(stage_labels[s] for s in stages) if stages else "No mapped workflow stage"
            items_html.append(
                f'<li class="capability-row">'
                f'<label><input type="checkbox" class="cap-switch" data-cap-id="{html.escape(cid, quote=True)}" '
                f'data-stages="{stage_attr}" checked> '
                f'<span class="cap-name">{html.escape(cid)}</span></label>'
                f'{detail_html}'
                f'<span class="cap-stages">Stages: {html.escape(stages_text)}</span>'
                f'</li>'
            )
        cap_sections_html.append(
            f'<details class="cap-group" open>'
            f'<summary>{html.escape(GROUP_LABELS[group])} ({len(entries)})</summary>'
            f'<ul>{"".join(items_html)}</ul>'
            f'</details>'
        )

    stage_cards = []
    for stage in mapping["stages"]:
        sid = stage["id"]
        label = stage["label"]
        caps = stage.get("capability_ids", [])
        cap_attr = html.escape(json.dumps(caps))
        cap_text = ", ".join(caps) if caps else "No selected capability"
        stage_cards.append(
            f'<article class="stage-card" data-stage-id="{html.escape(sid, quote=True)}" '
            f'data-cap-ids="{cap_attr}">'
            f'<h3>{html.escape(label)}</h3>'
            f'<p class="stage-caps">{html.escape(cap_text)}</p>'
            f'<p class="stage-status" aria-live="polite">No disabled mapped dependencies (preview)</p>'
            f'</article>'
        )

    all_caps_json = json.dumps(all_caps, ensure_ascii=False).replace("<", "\\u003c")
    stages_json = json.dumps(stage_caps, ensure_ascii=False).replace("<", "\\u003c")

    return f"""
<section class="panel notice" aria-live="polite" id="preview-notice">
  <strong>Preview only.</strong> This page is documentation. It does not change capabilities, permissions, memory, or runtime state.
</section>
<section class="panel" id="authority-summary" aria-labelledby="authority-heading">
  <h2 id="authority-heading">Environment and authority summary (always visible)</h2>
  <ul>
    <li>Identity: active <code>~/.hermes/SOUL.md</code> is a symlink to canonical <code>docs/profiles/secretary/SOUL.md</code>; that file is the maintained source, not a snapshot.</li>
    <li>Shared rules: <code>~/.agents/SOUL.md</code> and <code>USER.md</code> are pointers, not generated by capabilities.</li>
    <li>Workspace: <code>~/.agents</code> is read-write only for scoped tasks; other Spaces are read-only.</li>
    <li>Exception: bounded, preapproved Hermes runtime/profile maintenance only.</li>
    <li>Tai approval gates: commits, destructive operations, publication/external sharing, scientific acceptance, Hermes configuration.</li>
    <li>Memory: Hindsight desired bank <code>admin</code>; observed session bank <code>hermes</code>; <code>localhost:8888</code> failure unresolved, not configured/healthy.</li>
  </ul>
  <p class="live-status">Switches below are preview only and do not hide or alter this summary.</p>
</section>
<div class="grid">
  <section class="panel">
    <h2>Workflow stages</h2>
    <div class="stage-list" id="stage-list">
      {"".join(stage_cards)}
    </div>
    <p class="live-status" id="live-status" aria-live="polite">All capabilities enabled (preview).</p>
    <button type="button" id="reset-all">Reset all (preview)</button>
  </section>
  <section class="panel">
    <h2>Capabilities</h2>
    {"".join(cap_sections_html)}
  </section>
</div>
<style>
  .panel {{ background:#ffffff; border:1px solid #d1d5db; border-radius:.75rem; padding:1rem; margin-bottom:1rem; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  h1,h2 {{ margin:0 0 .5rem; }}
  .notice {{ border-left:4px solid #f59e0b; padding:.75rem; background:rgba(245,158,11,.12); border-radius:.5rem; }}
  .grid {{ display:grid; grid-template-columns:1fr; gap:1rem; }}
  @media (min-width:1024px) {{ .grid {{ grid-template-columns:2fr 1fr; }} }}
  .stage-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:.75rem; }}
  .stage-card {{ background:#f8fafc; border:1px solid #cbd5e1; border-radius:.5rem; padding:.75rem; }}
  .stage-card.affected {{ border-color:#f59e0b; background:rgba(245,158,11,.12); }}
  .stage-status {{ font-size:.85rem; margin:.25rem 0 0; color:#475569; }}
  .cap-group {{ margin-bottom:.75rem; }}
  .cap-group ul {{ list-style:none; padding-left:0; margin:.5rem 0 0; }}
  .capability-row {{ padding:.5rem 0; border-bottom:1px solid #e2e8f0; }}
  .cap-name {{ font-weight:600; }}
  .cap-detail {{ display:block; font-size:.85rem; color:#475569; }}
  .cap-stages {{ display:block; font-size:.8rem; color:#64748b; }}
  .empty-category {{ font-style:italic; color:#64748b; }}
  button {{ padding:.5rem .75rem; border-radius:.5rem; border:1px solid #94a3b8; background:#fff; cursor:pointer; }}
  .live-status {{ min-height:1.25rem; font-size:.9rem; color:#0f766e; }}
  [data-node-id].affected {{ outline:3px solid #f59e0b; outline-offset:2px; }}
  @media (prefers-color-scheme:dark) {{
    .panel {{ background:#111827; border-color:#334155; color:#e2e8f0; }}
    .stage-card {{ background:#1e293b; border-color:#475569; }}
    .stage-card.affected {{ background:rgba(245,158,11,.18); }}
    .stage-status,.cap-detail {{ color:#cbd5e1; }}
    .cap-stages,.empty-category {{ color:#94a3b8; }}
    .cap-group summary,.cap-name {{ color:#e2e8f0; }}
    button {{ background:#1e293b; color:#e2e8f0; border-color:#475569; }}
    .live-status {{ color:#5eead4; }}
  }}
</style>
<script>
const capabilityIds = {json.dumps(all_caps, ensure_ascii=False).replace("<", "\\u003c")};
const stageCaps = {json.dumps(stage_caps, ensure_ascii=False).replace("<", "\\u003c")};
function affectedStageIds(disabledCaps) {{
  const result = new Set();
  for (const [stageId, caps] of Object.entries(stageCaps)) {{
    if (caps.some(cap => disabledCaps.has(cap))) result.add(stageId);
  }}
  return result;
}}
function updatePreview() {{
  const disabled = new Set();
  document.querySelectorAll('.cap-switch').forEach(cb => {{
    if (!cb.checked) disabled.add(cb.dataset.capId);
  }});
  const affected = affectedStageIds(disabled);
  document.querySelectorAll('.stage-card').forEach(card => {{
    const stageId = card.dataset.stageId;
    const isAffected = affected.has(stageId);
    card.classList.toggle('affected', isAffected);
    const status = card.querySelector('.stage-status');
    if (isAffected) {{
      const deps = JSON.parse(card.dataset.capIds || '[]').filter(c => disabled.has(c));
      status.textContent = 'Affected (preview): ' + deps.join(', ') + ' disabled. Not assessed for replacement.';
    }} else {{
      status.textContent = 'No disabled mapped dependencies (preview)';
    }}
  }});
  document.querySelectorAll('[data-node-id]').forEach(node => {{
    const nodeId = node.dataset.nodeId;
    node.classList.toggle('affected', affected.has(nodeId));
  }});
  const live = document.getElementById('live-status');
  if (disabled.size === 0) {{
    live.textContent = 'All capabilities enabled (preview).';
  }} else {{
    live.textContent = 'Preview update: ' + disabled.size + ' capability switch(es) disabled; ' + affected.size + ' stage(s) affected. No runtime change.';
  }}
}}
document.querySelectorAll('.cap-switch').forEach(cb => cb.addEventListener('change', updatePreview));
const resetBtn = document.getElementById('reset-all');
if (resetBtn) resetBtn.addEventListener('click', () => {{
  document.querySelectorAll('.cap-switch').forEach(cb => {{ cb.checked = true; }});
  updatePreview();
}});
updatePreview();
</script>
"""


def build_html(data: dict[str, Any], mapping: dict[str, Any], workflow_html: str | None = None, environment_html: str | None = None) -> str:
    repo_root = REPO_ROOT
    bp = baseline_path(repo_root)
    baseline = bp.read_text(encoding="utf-8")
    # mark the primary graph
    baseline = baseline.replace("<svg ", '<svg id="secretary-primary-graph" ', 1)
    markup = _controls_markup(data, mapping)
    # inject controls before </body>
    injected = baseline.replace("</body>", markup + "\n</body>", 1)
    return injected


def build_explorer(repo_root: Path | str = REPO_ROOT) -> dict[str, Any]:
    repo_root = Path(repo_root)
    src = yaml_path(repo_root)
    text = src.read_text(encoding="utf-8")
    data = pc.load_yaml_text(text)
    pc.validate(data, PROFILE)
    mapping_file = mapping_path(repo_root)
    mapping = load_mapping(mapping_file)
    valid_ids = capability_ids_from_yaml(data)
    validate_mapping(mapping, valid_ids)
    html_text = build_html(data, mapping)
    out = output_path(repo_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    return {
        "profile": PROFILE,
        "output": str(out),
        "capabilities": sorted(valid_ids),
        "stages": [s["id"] for s in mapping["stages"]],
    }


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=None)
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root) if args.repo_root else REPO_ROOT
    result = build_explorer(repo_root)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
