#!/usr/bin/env python3
"""
Validates a launchd automation setup for compliance, syntax, permissions, and exit codes.
Usage:
    python3 verify_automation.py /path/to/my-space/automation/job-name [--kickstart]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def check_file(path: Path, desc: str, required: bool = True) -> bool:
    if path.exists():
        print(f" [PASS] {desc}: {path.name}")
        return True
    else:
        status = "[FAIL]" if required else "[WARN]"
        print(f" {status} {desc} is missing: {path}")
        return not required

def main():
    parser = argparse.ArgumentParser(description="Verify launchd automation directory")
    parser.add_argument("service_dir", help="Path to the service directory")
    parser.add_argument("--kickstart", action="store_true", help="Trigger service via launchctl kickstart and test exit code")
    parser.add_argument("--dry-run", action="store_true", help="Run scripts/run.sh directly and assert exit 0")
    args = parser.parse_args()

    service_dir = Path(args.service_dir).resolve()
    if not service_dir.is_dir():
        print(f"❌ Error: {service_dir} is not a directory.")
        sys.exit(1)

    print(f"\n🔍 Verifying launchd automation directory: {service_dir}")
    print("=" * 60)

    all_passed = True

    # 1. Check directory structure
    scripts_dir = service_dir / "scripts"
    logs_dir = service_dir / "logs"
    all_passed &= check_file(scripts_dir, "Scripts directory")
    all_passed &= check_file(logs_dir, "Logs directory")

    # 2. Check documentation contracts
    readme = service_dir / "README.md"
    agents = service_dir / "AGENTS.md"
    all_passed &= check_file(readme, "Human Runbook (README.md)")
    all_passed &= check_file(agents, "Agent Contract (AGENTS.md)")

    # 3. Check runner script & permissions
    runner = scripts_dir / "run.sh"
    if check_file(runner, "Runner script (scripts/run.sh)"):
        if os.access(runner, os.X_OK):
            print(f" [PASS] Executable permissions set on {runner.name}")
        else:
            print(f"❌ [FAIL] {runner.name} is not executable! Run: chmod +x {runner}")
            all_passed = False

    # 4. Check plist file & plutil lint
    plists = list(service_dir.glob("*.plist"))
    if not plists:
        print("❌ [FAIL] No *.plist file found in service directory.")
        all_passed = False
    else:
        for plist in plists:
            code, out, err = run_cmd(["plutil", "-lint", str(plist)])
            if code == 0:
                print(f" [PASS] Plist syntax valid (plutil -lint): {plist.name}")
            else:
                print(f"❌ [FAIL] Plist syntax error in {plist.name}: {err or out}")
                all_passed = False

    # 5. Check logs .gitignore
    gitignore = logs_dir / ".gitignore"
    if not gitignore.exists():
        print(f"⚠️  [WARN] Missing {gitignore}. Log files might accidentally be committed to git.")
    else:
        print(f" [PASS] Logs directory gitignored ({gitignore.name})")

    # 6. Check launchd status if deployed
    if plists:
        label = plists[0].stem
        uid = os.getuid()
        code, out, err = run_cmd(["launchctl", "list"])
        if code == 0 and label in out:
            print(f" [PASS] Service is loaded in launchd ({label})")
            # Extract exit status from launchctl list
            for line in out.splitlines():
                if label in line:
                    parts = line.split()
                    pid = parts[0]
                    status = parts[1]
                    print(f"        Status: PID={pid}, Last Exit Status={status}")
                    if status != "0" and pid == "-":
                        print(f"⚠️      Warning: Service last exited with code {status}!")
        else:
            print(f"ℹ️  [INFO] Service is not currently loaded in launchd.")

    # 7. Optional Dry-Run
    if args.dry_run and runner.exists():
        print("\n🚀 Executing test dry-run (bash scripts/run.sh)...")
        code, out, err = run_cmd(["/bin/bash", str(runner)])
        if code == 0:
            print(" [PASS] Dry-run executed successfully with exit code 0.")
        else:
            print(f"❌ [FAIL] Dry-run exited with code {code}!")
            if err:
                print(f"        Error output:\n{err}")
            all_passed = False

    # 8. Optional Kickstart
    if args.kickstart and plists:
        label = plists[0].stem
        print(f"\n⚡ Kickstarting service via launchctl ({label})...")
        code, out, err = run_cmd(["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{label}"])
        if code == 0:
            print(f" [PASS] Service kickstarted successfully.")
        else:
            print(f"❌ [FAIL] Kickstart failed: {err}")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print(" Verification SUCCEEDED. Automation conforms to LifeOS standards.")
        sys.exit(0)
    else:
        print("❌ Verification FAILED. Please resolve the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
