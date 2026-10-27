#!/usr/bin/env python3
"""Unified CLI for Bot Management: observe, apply, verify, and pull.

Usage:
  bot-ctl observe <bot> [--category <cat>]
  bot-ctl apply <bot> [--dry-run] [--no-smoke]
  bot-ctl verify [bot] [--category <cat>]
  bot-ctl pull plugins [--write]

Also supports flag-based dispatch:
  bot-ctl --observe [bot] [--category <cat>]
  bot-ctl --apply [bot] [--dry-run]
  bot-ctl --verify [bot]
  bot-ctl --pull plugins
"""
import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BOTS = Path(os.environ.get("BOTS_DIR", "~/.agents/bots")).expanduser()
PROFILES = Path(os.environ.get("HERMES_PROFILES", "~/.hermes/profiles")).expanduser()


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "COLUMNS": "300"})
    return r.returncode, (r.stdout + r.stderr)


def make_hermes_runner(bot):
    def runner(*args):
        return sh(["hermes", "-p", bot, *args])
    return runner


def parse_models(models_path):
    text = Path(models_path).read_text()
    providers, aliases = {}, {}
    prov, cat = None, None
    section = None
    for line in text.splitlines():
        if re.match(r"^providers:", line):
            section = "p"
            continue
        if re.match(r"^aliases:", line):
            section = "a"
            continue
        if section == "p":
            m = re.match(r"^  ([\w-]+):\s*$", line)
            if m:
                prov = m.group(1)
                continue
            m = re.match(r"^\s+- ([\w.-]+)", line)
            if m and prov:
                providers[m.group(1)] = prov
        elif section == "a":
            m = re.match(r"^  (\w+):\s*$", line)
            if m:
                cat = m.group(1)
                continue
            m = re.match(r"^    (\w+):\s*(.*)$", line)
            if m and cat:
                val = m.group(2).strip()
                mm = re.search(r"model:\s*([\w.-]+)", val)
                ee = re.search(r"effort:\s*(\w+)", val)
                aliases[f"{cat}.{m.group(1)}"] = (mm.group(1), ee.group(1) if ee else None) if mm else None
    return providers, aliases


def frontmatter(text):
    parts = text.split("---")
    return parts[1] if len(parts) > 2 and text.startswith("---") else ""


def table_rows(out):
    res = []
    for l in out.splitlines():
        if l.startswith("│") and not l.startswith("│  "):
            cells = [c.strip() for c in l.strip("│").split("│")]
            if len(cells) >= 2 and cells[0]:
                res.append(cells)
    return res


def cfg_get(bot, key, hermes_fn):
    code, out = hermes_fn("config", "get", key)
    if code:
        return None
    vals = [l for l in out.splitlines() if l.strip() and not l.lstrip().startswith(("⚠", "Did you mean", "(Use"))]
    return vals[-1].strip() if vals else ""


def _skills_config(cfg, cfg_path):
    skills = cfg.get("skills")
    if not isinstance(skills, dict) or not isinstance(skills.get("external_dirs"), list):
        raise ValueError(f"{cfg_path}: 'skills' must be {{\"external_dirs\": [...]}}")
    return skills


def resolve_bot_config(bot_dir, models_path):
    bot_dir = Path(bot_dir)
    soul_path = bot_dir / "SOUL.md"
    if not soul_path.exists():
        raise FileNotFoundError(f"{soul_path} does not exist")
    cfg_path = bot_dir / "config.json"
    if not cfg_path.exists():
        raise FileNotFoundError(f"{cfg_path} does not exist")

    cfg = json.loads(cfg_path.read_text())
    providers, aliases = parse_models(models_path)

    prim_alias = cfg.get("model", {}).get("primary")
    if not prim_alias or prim_alias not in aliases:
        raise ValueError(f"Primary model alias '{prim_alias}' not found in {models_path}")

    res = aliases[prim_alias]
    if not res:
        raise ValueError(f"Alias '{prim_alias}' resolves to null")

    model_name, effort = res
    provider = providers.get(model_name)
    if not provider:
        raise ValueError(f"Model '{model_name}' has no registered provider in {models_path}")

    return {
        "bot_name": bot_dir.name,
        "bot_dir": bot_dir,
        "model": {
            "primary_alias": prim_alias,
            "default": model_name,
            "provider": provider,
            "effort": effort,
            "fallback": cfg.get("model", {}).get("fallback", [])
        },
        "skills": _skills_config(cfg, cfg_path),
        "plugins": cfg.get("plugins", {}),
        "mcps": cfg.get("mcps", {}),
        "memory": cfg.get("memory", {})
    }


def _observe_skills(cfg, hermes_fn, add):
    code, out = hermes_fn("config", "get", "skills.external_dirs")
    live = sorted(str(Path(l.strip()[2:].strip()).expanduser()) for l in out.splitlines() if l.strip().startswith("- "))
    want = sorted(_ext_dirs(cfg))
    add("skills", "skills.external_dirs", "match" if live == want else "drift", f"want={want} got={live}")
    missing = [d for d in want if not Path(d).is_dir()]
    add("skills", "skills folders exist", "match" if not missing else "missing", f"missing={missing}")


def observe_bot(bot_dir, models_path, profile_dir, hermes_fn, category=None):
    bot_dir = Path(bot_dir)
    profile_dir = Path(profile_dir)
    bot = bot_dir.name
    rows = []

    def add(cat, check, status, detail=""):
        if category and category.lower() not in ("all", cat.lower()):
            return
        rows.append({"category": cat, "bot": bot, "check": check, "status": status, "detail": detail})

    # SOUL
    soul = bot_dir / "SOUL.md"
    if not soul.exists():
        add("soul", "SOUL.md exists", "missing")
    else:
        s = soul.read_text()
        fm = frontmatter(s)
        miss = [k for k in ("name", "title", "description", "instruction", "enable") if not re.search(rf"^{k}:", fm, re.M)]
        add("soul", "SOUL frontmatter", "match" if not miss else "drift", ",".join(miss))
        add("soul", "SOUL sections", "match" if "## Context" in s and "## Model" not in s and "dirs:" not in fm else "drift",
            "needs ## Context, no ## Model, no dirs")
        link = profile_dir / "SOUL.md"
        ok = link.is_symlink() and link.resolve() == soul.resolve()
        add("soul", "SOUL symlink", "match" if ok else ("missing" if not link.exists() and not link.is_symlink() else "drift"), str(link))

    # Config & Models
    cfg_path = bot_dir / "config.json"
    if not cfg_path.exists():
        add("models", "config.json", "missing")
        return rows
    cfg = json.loads(cfg_path.read_text())
    providers, aliases = parse_models(models_path)

    prim = cfg.get("model", {}).get("primary")
    res = aliases.get(prim)
    if res is None:
        add("models", "model alias", "missing", f"{prim} not resolvable")
    else:
        model, effort = res
        live = cfg_get(bot, "model.default", hermes_fn)
        lp = cfg_get(bot, "model.provider", hermes_fn)
        add("models", "model.default", "match" if live == model else "drift", f"want {model} got {live}")
        want_p = providers.get(model)
        add("models", "model.provider", "match" if live and lp == want_p else "drift", f"want {want_p} got {lp}")
        add("models", "effort", "untested", f"want {effort}; runtime key unconfirmed")

    for fb in cfg.get("model", {}).get("fallback", []):
        add("models", f"fallback {fb}", "match" if aliases.get(fb) else "missing", "format of fallback_providers untested")

    # Skills
    _observe_skills(cfg, hermes_fn, add)

    # Plugins
    code, out = hermes_fn("plugins", "list")
    pl = {}
    for c in table_rows(out):
        if len(c) > 1 and c[1] in ("enabled", "disabled", "not enabled"):
            pl.setdefault(c[0], c[1])
    pcfg = cfg.get("plugins", {})
    for nme in pcfg.get("enable", []):
        add("plugins", f"plugin {nme}", "match" if pl.get(nme) == "enabled" else "drift", pl.get(nme, "not found"))
    for g in pcfg.get("disable_groups", []):
        on = sorted(n for n, st in pl.items() if st == "enabled" and fnmatch.fnmatch(n, g))
        add("plugins", f"plugins off {g}", "match" if not on else "drift", ",".join(on))

    # MCP
    code, out = hermes_fn("mcp", "list")
    mc = {}
    for l in out.splitlines():
        m = re.match(r"^\s+([\w-]+)\s{2,}.*?([✓✗])\s+(\w+)\s*$", l)
        if m:
            mc[m.group(1)] = m.group(3)
    want_m = set(cfg.get("mcps", {}).get("enable", []))
    for nme, st in mc.items():
        ok = (st == "enabled") == (nme in want_m)
        add("mcp", f"mcp {nme}", "match" if ok else "drift", f"{st}; want {'on' if nme in want_m else 'off'}")
    for nme in want_m - set(mc):
        add("mcp", f"mcp {nme}", "missing", "not configured in profile")

    # Memory
    want_mem = cfg.get("memory", {}).get("provider", "")
    live_mem = cfg_get(bot, "memory.provider", hermes_fn)
    add("memory", "memory.provider", "match" if (live_mem or "built-in") == want_mem else "drift",
        f"want {want_mem} got {live_mem or 'built-in'}")

    return rows


def reconcile_soul_symlink(soul_path, profile_dir):
    soul_path = Path(soul_path).resolve()
    profile_dir = Path(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)
    target = profile_dir / "SOUL.md"

    if target.is_symlink() or target.exists():
        if target.is_symlink() and target.resolve() == soul_path:
            return target
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)

    target.symlink_to(soul_path)
    return target


def backup_profile(profile_dir, backup_root=None):
    profile_dir = Path(profile_dir)
    if not profile_dir.exists():
        raise FileNotFoundError(f"Profile directory {profile_dir} does not exist")

    if backup_root is None:
        backup_root = profile_dir / "backups"
    backup_root = Path(backup_root)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    dest = backup_root / timestamp
    dest.mkdir(parents=True, exist_ok=True)

    for item in profile_dir.iterdir():
        if item.name in (".env", "backups"):
            continue
        target_path = dest / item.name
        if item.is_dir() and not item.is_symlink():
            shutil.copytree(item, target_path, symlinks=True)
        else:
            shutil.copy2(item, target_path, follow_symlinks=False)

    return dest


APPLY_STEPS = ("soul", "model", "skills", "memory")


def _ext_dirs(cfg):
    return [str(Path(d).expanduser()) for d in cfg["skills"]["external_dirs"]]


def _check_skill_dirs(cfg):
    # Pre-flight, before any write: a missing folder would make Hermes load nothing without saying so.
    missing = [d for d in _ext_dirs(cfg) if not Path(d).is_dir()]
    if missing:
        raise ValueError(f"skills.external_dirs not found: {missing}")


def _apply_skills(cfg, hermes_fn):
    # Skills are not listed per bot. Hermes reads every skill in these folders; Tai toggles each skill live.
    hermes_fn("config", "set", "skills.external_dirs", json.dumps(_ext_dirs(cfg)))


def apply_bot(bot_dir, models_path, profile_dir, hermes_fn, dry_run=False, skip_smoke=False, only=None):
    steps = set(only) if only else set(APPLY_STEPS)
    if not steps <= set(APPLY_STEPS):
        raise ValueError(f"Unknown apply step(s): {sorted(steps - set(APPLY_STEPS))}")

    bot_dir = Path(bot_dir)
    profile_dir = Path(profile_dir)
    cfg = resolve_bot_config(bot_dir, models_path)
    bot = cfg["bot_name"]

    if dry_run:
        return {
            "success": True,
            "bot": bot,
            "dry_run": True,
            "config": cfg
        }

    if "skills" in steps:
        _check_skill_dirs(cfg)

    # 1. Backup
    backup_dir = backup_profile(profile_dir)

    # 2. SOUL symlink
    if "soul" in steps:
        reconcile_soul_symlink(bot_dir / "SOUL.md", profile_dir)

    # 3. Model
    if "model" in steps:
        hermes_fn("config", "set", "model.default", cfg["model"]["default"])
        hermes_fn("config", "set", "model.provider", cfg["model"]["provider"])
        if cfg["model"]["effort"]:
            hermes_fn("config", "set", "model.effort", cfg["model"]["effort"])

    # 4. Skills
    if "skills" in steps:
        _apply_skills(cfg, hermes_fn)

    # 5. Memory
    if "memory" in steps and "provider" in cfg["memory"]:
        hermes_fn("config", "set", "memory.provider", cfg["memory"]["provider"])

    # 6. Smoke test
    smoke_msg = ""
    if not skip_smoke:
        code, out = hermes_fn("chat", "-q", "say hi")
        smoke_msg = out.strip()
        if code != 0:
            return {
                "success": False,
                "bot": bot,
                "backup_dir": backup_dir,
                "error": f"Smoke test failed: {smoke_msg}"
            }

    return {
        "success": True,
        "bot": bot,
        "backup_dir": backup_dir,
        "smoke": smoke_msg
    }


def verify_bot(bot_dir, models_path, profile_dir, hermes_fn, category=None):
    rows = observe_bot(bot_dir, models_path, profile_dir, hermes_fn, category=category)
    bad = [r for r in rows if r["status"] in ("drift", "missing")]
    exit_code = 1 if bad else 0
    return exit_code, rows


def pull_plugins(hermes_fn, plugins_yaml_path):
    catalog = {
        "plugins": {},
        "mcps": {},
        "memory_providers": []
    }

    # 1. plugins list
    code, out = hermes_fn("plugins", "list")
    if code == 0:
        for row in table_rows(out):
            if row[0] == "Name":
                continue
            name = row[0]
            status = row[1] if len(row) > 1 else ""
            desc = row[2] if len(row) > 2 else ""
            catalog["plugins"][name] = {"status": status, "description": desc}

    # 2. mcp list
    code, out = hermes_fn("mcp", "list")
    if code == 0:
        for line in out.splitlines():
            m = re.match(r"^\s+([\w-]+)\s{2,}.*?([✓✗])\s+(\w+)\s*$", line)
            if m:
                catalog["mcps"][m.group(1)] = m.group(3)

    # 3. memory
    code, out = hermes_fn("memory", "--help")
    if code == 0:
        for line in out.splitlines():
            if "providers:" in line.lower():
                parts = re.split(r"[:;,]", line, maxsplit=1)
                if len(parts) > 1:
                    catalog["memory_providers"] = [p.strip() for p in parts[1].split() if p.strip()]

    # Diff with current plugins.yaml
    diff = {"plugins_added": [], "plugins_removed": []}
    p_path = Path(plugins_yaml_path)
    if p_path.exists():
        text = p_path.read_text()
        known = set(re.findall(r"^\s{4}([\w-]+):", text, re.M))
        for p in catalog["plugins"]:
            if p not in known:
                diff["plugins_added"].append(p)

    return catalog, diff


def format_table(rows):
    if not rows:
        return "No checks executed."
    w_cat = max(len(r["category"]) for r in rows)
    w_check = max(len(r["check"]) for r in rows)
    w_stat = max(len(r["status"]) for r in rows)
    lines = []
    for r in rows:
        lines.append(f"{r['bot']:8} | {r['category']:{w_cat}} | {r['check']:{w_check}} | {r['status']:{w_stat}} | {r['detail']}")
    return "\n".join(lines)


def main_cli(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    # Support flag-based dispatch: convert --observe to observe, etc.
    normalized = []
    for arg in argv:
        if arg in ("--observe", "-observe"): normalized.append("observe")
        elif arg in ("--apply", "-apply"): normalized.append("apply")
        elif arg in ("--verify", "-verify"): normalized.append("verify")
        elif arg in ("--pull", "-pull"): normalized.append("pull")
        else: normalized.append(arg)

    parser = argparse.ArgumentParser(prog="bot-ctl", description="Unified Bot Management CLI.")
    subparsers = parser.add_subparsers(dest="command")

    # observe
    p_obs = subparsers.add_parser("observe", help="Inspect bot configuration vs live Hermes profile.")
    p_obs.add_argument("bot", nargs="?", help="Bot name (e.g. harvey, donna)")
    p_obs.add_argument("--category", "-c", help="Category: soul, models, skills, plugins, mcp, memory")

    # apply
    p_app = subparsers.add_parser("apply", help="Reconcile declarative config to live Hermes profile.")
    p_app.add_argument("bot", nargs="?", help="Bot name to apply")
    p_app.add_argument("--dry-run", action="store_true", help="Print actions without modifying files or profile")
    p_app.add_argument("--no-smoke", action="store_true", help="Skip running the live smoke test")
    p_app.add_argument("--only", help="Comma-separated steps to apply: soul,model,skills,memory (default: all)")

    # verify
    p_ver = subparsers.add_parser("verify", help="Strict verification of bot state against config.")
    p_ver.add_argument("bot", nargs="?", help="Bot name to verify")
    p_ver.add_argument("--category", "-c", help="Category filter")

    # pull
    p_pul = subparsers.add_parser("pull", help="Pull live catalog (e.g. plugins) from Hermes.")
    p_pul.add_argument("target", choices=["plugins", "all"], default="plugins", nargs="?", help="Target catalog to pull")
    p_pul.add_argument("--write", action="store_true", help="Write updates to plugins.yaml")

    args = parser.parse_args(normalized)
    if not args.command:
        parser.print_help()
        sys.exit(0)

    models_path = BOTS / "models.yaml"
    plugins_path = BOTS / "plugins.yaml"

    # Locate bot directories
    bot_dirs = sorted(p.parent for p in BOTS.glob("*/*/SOUL.md"))
    if getattr(args, "bot", None):
        bot_dirs = [d for d in bot_dirs if d.name == args.bot]
        if not bot_dirs:
            sys.exit(f"Bot '{args.bot}' not found in {BOTS}")

    if args.command == "observe":
        all_rows = []
        for bd in bot_dirs:
            runner = make_hermes_runner(bd.name)
            p_dir = PROFILES / bd.name
            rows = observe_bot(bd, models_path, p_dir, runner, category=args.category)
            all_rows.extend(rows)
        print(format_table(all_rows))
        sys.exit(0)

    elif args.command == "verify":
        total_exit = 0
        all_rows = []
        for bd in bot_dirs:
            runner = make_hermes_runner(bd.name)
            p_dir = PROFILES / bd.name
            code, rows = verify_bot(bd, models_path, p_dir, runner, category=args.category)
            all_rows.extend(rows)
            if code != 0:
                total_exit = 1
        print(format_table(all_rows))
        bad = [r for r in all_rows if r["status"] in ("drift", "missing")]
        print(f"\n{len(all_rows)} checks, {len(bad)} drift or missing.")
        sys.exit(total_exit)

    elif args.command == "apply":
        for bd in bot_dirs:
            runner = make_hermes_runner(bd.name)
            p_dir = PROFILES / bd.name
            print(f"Applying bot '{bd.name}'...")
            only = args.only.split(",") if args.only else None
            res = apply_bot(bd, models_path, p_dir, runner, dry_run=args.dry_run, skip_smoke=args.no_smoke, only=only)
            if not res["success"]:
                sys.exit(f"Apply failed for {bd.name}: {res.get('error')}")
            if args.dry_run:
                print(f"[{bd.name}] DRY-RUN successful.")
            else:
                print(f"[{bd.name}] Successfully applied. Backup at: {res['backup_dir']}")
                if res.get("smoke"):
                    print(f"[{bd.name}] Smoke test: {res['smoke'][:60]}...")
        if not args.dry_run:
            print("\nRunning post-apply verification...")
            step_category = {"soul": "soul", "model": "models", "skills": "skills", "memory": "memory"}
            categories = [step_category[s] for s in args.only.split(",")] if args.only else [None]
            for bd in bot_dirs:
                runner = make_hermes_runner(bd.name)
                p_dir = PROFILES / bd.name
                for category in categories:
                    code, rows = verify_bot(bd, models_path, p_dir, runner, category=category)
                    print(format_table(rows))
                    if code != 0:
                        sys.exit(1)
        sys.exit(0)

    elif args.command == "pull":
        # Pull catalog using default or first bot runner
        bot_name = bot_dirs[0].name if bot_dirs else "harvey"
        runner = make_hermes_runner(bot_name)
        catalog, diff = pull_plugins(runner, plugins_path)
        print(f"Discovered {len(catalog['plugins'])} plugins, {len(catalog['mcps'])} MCPs.")
        if diff["plugins_added"]:
            print(f"New plugins not in plugins.yaml: {', '.join(diff['plugins_added'])}")
        else:
            print("No new plugins found.")
        sys.exit(0)


if __name__ == "__main__":
    main_cli()
