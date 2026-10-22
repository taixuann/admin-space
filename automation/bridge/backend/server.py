"""Bridge Server: loopback HTTP server serving frontend and workspace inspection REST API."""

from __future__ import annotations

import json
import mimetypes
import os
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict

from scanner import inspect_git_workspace, scan_all_workspaces

BACKEND_DIR = Path(__file__).resolve().parent
BRIDGE_DIR = BACKEND_DIR.parent
FRONTEND_DIR = BRIDGE_DIR / "frontend"


def load_config() -> Dict[str, Any]:
    try:
        from config_manager import load_github_config, load_drive_config
        gh = load_github_config()
        dr = load_drive_config()
        return {
            "version": 1,
            "settings": gh.get("settings", {}),
            "workspaces": gh.get("workspaces", []),
            "drive_profiles": dr.get("profiles", []),
        }
    except Exception:
        return {"version": 1, "settings": {}, "workspaces": [], "drive_profiles": []}


def save_config(cfg: Dict[str, Any]) -> None:
    try:
        from config_manager import load_github_config, save_github_config, load_drive_config, save_drive_config
        if "workspaces" in cfg:
            gh = load_github_config()
            gh["workspaces"] = cfg["workspaces"]
            save_github_config(gh)
        if "drive_profiles" in cfg:
            dr = load_drive_config()
            dr["profiles"] = cfg["drive_profiles"]
            save_drive_config(dr)
    except Exception:
        pass


class BridgeRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        # Keep console output clean
        pass

    def send_json(self, status: int, data: Any) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        # REST API Endpoints
        if path == "/api/status":
            try:
                data = scan_all_workspaces(CONFIG_FILE)
                self.send_json(200, {"success": True, **data})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        if path == "/api/config":
            try:
                cfg = load_config()
                self.send_json(200, {"success": True, "config": cfg})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        if path == "/api/workspace/tree":
            try:
                import urllib.parse
                parsed = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed.query)
                target_path = params.get("path", [""])[0]
                from scanner import build_folder_tree
                tree = build_folder_tree(target_path, max_depth=2)
                self.send_json(200, {"success": True, "tree": tree})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        if path == "/api/drive/remote_tree":
            try:
                from scanner import fetch_gdrive_remote_tree, build_gdrive_remote_hierarchy
                dirs = fetch_gdrive_remote_tree("gdrive:")
                tree = build_gdrive_remote_hierarchy("gdrive:")
                self.send_json(200, {"success": True, "directories": dirs, "tree": tree})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        # Static file serving from frontend/
        req_file = "index.html" if path in ("/", "/index.html") else path.lstrip("/")
        target_path = (FRONTEND_DIR / req_file).resolve()

        # Security check: must reside inside FRONTEND_DIR
        try:
            target_path.relative_to(FRONTEND_DIR.resolve())
        except ValueError:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        if target_path.exists() and target_path.is_file():
            mime_type, _ = mimetypes.guess_type(str(target_path))
            content = target_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            req_data = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            self.send_json(400, {"success": False, "error": "Invalid JSON"})
            return

        if path == "/api/workspace/toggle":
            # Toggle automation or gcal tracking
            ws_id = req_data.get("id")
            field = req_data.get("field")  # "track_automation" or "track_gcal"
            val = req_data.get("value")

            if not ws_id or field not in ("track_automation", "track_gcal"):
                self.send_json(400, {"success": False, "error": "Invalid parameters"})
                return

            cfg = load_config()
            found = False
            for ws in cfg.get("workspaces", []):
                if ws.get("id") == ws_id:
                    ws[field] = bool(val)
                    found = True
                    break

            if found:
                save_config(cfg)
                self.send_json(200, {"success": True, "workspaces": scan_all_workspaces(CONFIG_FILE)})
            else:
                self.send_json(404, {"success": False, "error": f"Workspace {ws_id} not found"})
            return

        if path == "/api/workspace/fetch":
            # Run git fetch in the background for a workspace
            ws_id = req_data.get("id")
            cfg = load_config()
            target_ws = next((w for w in cfg.get("workspaces", []) if w.get("id") == ws_id), None)
            if not target_ws:
                self.send_json(404, {"success": False, "error": "Workspace not found"})
                return

            target_path = Path(os.path.expanduser(target_ws.get("path", "")))
            if not target_path.exists():
                self.send_json(400, {"success": False, "error": "Workspace path does not exist"})
                return

            try:
                proc = subprocess.run(
                    ["git", "fetch", "--prune"],
                    cwd=str(target_path),
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                git_info = inspect_git_workspace(str(target_path))
                self.send_json(200, {"success": True, "git": git_info, "fetch_out": proc.stdout or proc.stderr})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        if path == "/api/workspace/open":
            ws_id = req_data.get("id")
            cfg = load_config()
            target_ws = next((w for w in cfg.get("workspaces", []) if w.get("id") == ws_id), None)
            if not target_ws:
                self.send_json(404, {"success": False, "error": "Workspace not found"})
                return
            target_path = Path(os.path.expanduser(target_ws.get("path", "")))
            if not target_path.exists():
                self.send_json(400, {"success": False, "error": "Path does not exist"})
                return
            try:
                subprocess.run(["open", str(target_path)], check=False)
                self.send_json(200, {"success": True})
            except Exception as exc:
                self.send_json(500, {"success": False, "error": str(exc)})
            return

        if path == "/api/workspace/update":
            ws_id = req_data.get("id")
            updates = req_data.get("updates", {})
            cfg = load_config()
            workspaces = cfg.get("workspaces", [])
            target_ws = next((w for w in workspaces if w.get("id") == ws_id), None)

            allowed_fields = (
                "tracked",
                "name",
                "default_branch",
                "remote_repo",
                "category",
            )

            if target_ws is not None:
                for k in allowed_fields:
                    if k in updates:
                        target_ws[k] = updates[k]
            else:
                new_entry = {
                    "id": ws_id,
                    "name": updates.get("name") or ws_id.replace("-", " ").title(),
                    "category": updates.get("category") or "General",
                    "path": "",
                    "remote_repo": updates.get("remote_repo"),
                    "default_branch": updates.get("default_branch") or "main",
                    "tracked": updates.get("tracked", True),
                    "track_automation": updates.get("track_automation", False),
                }
                workspaces.append(new_entry)

            save_config(cfg)
            full_scan = scan_all_workspaces(CONFIG_FILE)
            self.send_json(200, {"success": True, **full_scan})
            return

        if path == "/api/drive/update":
            prof_id = req_data.get("id")
            updates = req_data.get("updates", {})
            cfg = load_config()
            profiles = cfg.get("drive_profiles", [])
            target_prof = next((p for p in profiles if p.get("id") == prof_id), None)

            allowed_fields = (
                "name",
                "category",
                "source_path",
                "remote_target",
                "include_folders",
                "exclude_patterns",
                "enabled",
            )

            if target_prof is not None:
                for k in allowed_fields:
                    if k in updates:
                        target_prof[k] = updates[k]
            else:
                new_prof = {
                    "id": prof_id or f"drive-{len(profiles)+1}",
                    "name": updates.get("name") or "New Drive Sync Profile",
                    "category": updates.get("category") or "Cloud Sync",
                    "source_path": updates.get("source_path") or "",
                    "remote_target": updates.get("remote_target") or "gdrive:",
                    "include_folders": updates.get("include_folders") or "*",
                    "exclude_patterns": updates.get("exclude_patterns") or ".git, .venv, .pytest_cache, .DS_Store",
                    "enabled": updates.get("enabled", True),
                    "last_synced": None,
                }
                profiles.append(new_prof)
                cfg["drive_profiles"] = profiles

            save_config(cfg)
            full_scan = scan_all_workspaces(CONFIG_FILE)
            self.send_json(200, {"success": True, **full_scan})
            return

        if path == "/api/drive/check":
            prof_id = req_data.get("id")
            cfg = load_config()
            profiles = cfg.get("drive_profiles", [])
            target_prof = next((p for p in profiles if p.get("id") == prof_id), None)
            if not target_prof:
                self.send_json(404, {"success": False, "error": "Profile not found"})
                return

            source = Path(os.path.expanduser(target_prof.get("source_path", "")))
            if not source.exists():
                self.send_json(400, {"success": False, "error": f"Source directory {source} does not exist"})
                return

            # Test rclone dry-run
            target = target_prof.get("remote_target", "")
            excludes = [p.strip() for p in (target_prof.get("exclude_patterns") or "").split(",") if p.strip()]
            rclone_args = ["rclone", "check", str(source), target, "--dry-run"]
            for exc in excludes:
                rclone_args.extend(["--exclude", exc])

            code, out, err = run_cmd(rclone_args, timeout=20)
            self.send_json(200, {"success": True, "output": out or err or "Check complete."})
            return

        self.send_json(404, {"success": False, "error": "Endpoint not found"})


def run_server(port: int = 8768) -> None:
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, BridgeRequestHandler)
    print(f"Bridge dashboard running at: http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Bridge server...")
        httpd.shutdown()


if __name__ == "__main__":
    import sys
    port = 8768
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
