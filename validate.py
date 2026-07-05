#!/usr/bin/env python3
"""
Composer plugin validator.

Checks the plugin installation, manifest, required files, Python environment,
and connector configuration before a live run. Exit code 0 = all checks pass,
1 = one or more failures.

Usage:
    python3 validate.py
    python3 validate.py --json    # machine-readable output
"""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET = "\033[0m"
GREEN = "\033[32m"
RED   = "\033[31m"
YELLOW = "\033[33m"
BOLD  = "\033[1m"

def ok(msg):   return f"{GREEN}✓{RESET}  {msg}"
def fail(msg): return f"{RED}✗{RESET}  {msg}"
def warn(msg): return f"{YELLOW}~{RESET}  {msg}"

# ── Helpers ───────────────────────────────────────────────────────────────────

def find_plugin_root() -> Path:
    """Walk up from cwd until we find .claude-plugin/plugin.json."""
    here = Path(__file__).resolve().parent
    for candidate in [here, *here.parents]:
        if (candidate / ".claude-plugin" / "plugin.json").exists():
            return candidate
    return here  # fallback: assume script is in root


def check_manifest(root: Path) -> tuple[bool, dict, list[str]]:
    path = root / ".claude-plugin" / "plugin.json"
    notes = []
    if not path.exists():
        return False, {}, [fail(".claude-plugin/plugin.json not found")]

    try:
        manifest = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return False, {}, [fail(f".claude-plugin/plugin.json is invalid JSON: {e}")]

    required = ["name", "version", "description", "author", "license"]
    for field in required:
        if field not in manifest:
            notes.append(fail(f"plugin.json missing required field: {field}"))

    if not notes:
        ver = manifest.get("version", "?")
        name = manifest.get("name", "?")
        notes.append(ok(f"plugin.json — {name} v{ver}"))
        return True, manifest, notes
    return False, manifest, notes


def check_required_files(root: Path) -> tuple[bool, list[str]]:
    required = [
        ".mcp.json",
        "README.md",
        "CHANGELOG.md",
        "CONNECTORS.md",
        "LICENSE",
        "skills/composer/SKILL.md",
        "commands/compose.md",
        "commands/assets.md",
        "commands/archive.md",
        "commands/setup.md",
    ]
    notes = []
    passed = True
    for rel in required:
        p = root / rel
        if p.exists():
            notes.append(ok(f"{rel}"))
        else:
            notes.append(fail(f"{rel} — missing"))
            passed = False
    return passed, notes


def check_mcp_json(root: Path) -> tuple[bool, list[str]]:
    path = root / ".mcp.json"
    if not path.exists():
        return False, [fail(".mcp.json not found")]

    try:
        cfg = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return False, [fail(f".mcp.json invalid JSON: {e}")]

    servers = cfg.get("mcpServers", {})
    notes = []

    if not servers:
        notes.append(warn(".mcp.json — no connectors configured yet "
                         "(add your visual asset system and/or archive in CONNECTORS.md)"))
        return True, notes  # not a failure — connectors are user-configured

    for name, conf in servers.items():
        has_type = "type" in conf
        has_url  = "url" in conf or "command" in conf
        if has_type and has_url:
            notes.append(ok(f"connector: {name} ({conf.get('type', 'stdio')})"))
        else:
            notes.append(warn(f"connector: {name} — incomplete config (needs type + url or command)"))

    return True, notes


def check_python_env() -> tuple[bool, list[str]]:
    notes = []
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 9):
        notes.append(fail(f"Python {major}.{minor} — 3.9+ required"))
        return False, notes
    notes.append(ok(f"Python {major}.{minor}"))

    # mcp package — optional but needed for the server
    if importlib.util.find_spec("mcp") is not None:
        try:
            import mcp
            ver = getattr(mcp, "__version__", "installed")
            notes.append(ok(f"mcp package — {ver}"))
        except Exception:
            notes.append(ok("mcp package — installed"))
    else:
        notes.append(warn("mcp package not installed — not required for skills-only use; "
                         "run: pip install mcp  if you need the MCP server"))

    return True, notes


def check_connector_detection(root: Path) -> tuple[bool, list[str]]:
    """
    Simulate the capability-detection logic Composer uses at runtime.
    Reads .mcp.json and reports what Composer would detect.
    """
    path = root / ".mcp.json"
    notes = []
    if not path.exists():
        return True, [warn("skipped — .mcp.json not found")]

    try:
        cfg = json.loads(path.read_text())
    except Exception:
        return True, [warn("skipped — .mcp.json unreadable")]

    servers = cfg.get("mcpServers", {})
    if not servers:
        notes.append(warn("No connectors configured — Composer will run web-search-only mode"))
        notes.append(warn("Add connectors to .mcp.json; see CONNECTORS.md"))
        return True, notes

    # In a live run, Composer inspects each server's exposed tools.
    # Here we check for the structural signals we can read without running the servers.
    VISUAL_SIGNALS = {"image", "asset", "media", "photo", "crop", "thumbnail",
                      "transform", "similarity", "dam", "cloudinary", "bynder"}
    ARCHIVE_SIGNALS = {"file", "drive", "doc", "search_files", "list_files",
                       "create_file", "write_file", "notion", "confluence"}

    visual_servers = []
    archive_servers = []
    other_servers = []

    for name, conf in servers.items():
        name_lower = name.lower()
        url_lower = (conf.get("url") or "").lower()
        combined = name_lower + " " + url_lower

        is_visual  = any(s in combined for s in VISUAL_SIGNALS)
        is_archive = any(s in combined for s in ARCHIVE_SIGNALS)

        if is_visual:
            visual_servers.append(name)
        elif is_archive:
            archive_servers.append(name)
        else:
            other_servers.append(name)

    if visual_servers:
        notes.append(ok(f"visual asset system likely: {', '.join(visual_servers)} "
                       "(confirmed at runtime by tool inspection)"))
    else:
        notes.append(warn("no visual asset server detected — /assets and /compose visual layer unavailable"))

    if archive_servers:
        notes.append(ok(f"archive system likely: {', '.join(archive_servers)} "
                       "(confirmed at runtime by tool inspection)"))
    else:
        notes.append(warn("no archive server detected — /archive and package saving unavailable"))

    if other_servers:
        notes.append(warn(f"unclassified servers: {', '.join(other_servers)} "
                         "(Composer will classify by tool inspection at runtime)"))

    return True, notes


# ── Main ──────────────────────────────────────────────────────────────────────

def run_checks(as_json: bool = False):
    root = find_plugin_root()
    results = {}

    sections = [
        ("Plugin manifest",    lambda: check_manifest(root)),
        ("Required files",     lambda: check_required_files(root)),
        ("MCP configuration",  lambda: check_mcp_json(root)),
        ("Python environment", lambda: check_python_env),
        ("Connector detection",lambda: check_connector_detection(root)),
    ]

    all_pass = True
    report = {}

    # Run checks
    manifest_ok, manifest, manifest_notes = check_manifest(root)
    files_ok,    files_notes              = check_required_files(root)
    mcp_ok,      mcp_notes               = check_mcp_json(root)
    python_ok,   python_notes            = check_python_env()
    detect_ok,   detect_notes            = check_connector_detection(root)

    checks = [
        ("Plugin manifest",     manifest_ok, manifest_notes),
        ("Required files",      files_ok,    files_notes),
        ("MCP configuration",   mcp_ok,      mcp_notes),
        ("Python environment",  python_ok,   python_notes),
        ("Connector detection", detect_ok,   detect_notes),
    ]

    if as_json:
        output = {}
        for title, passed, notes in checks:
            output[title] = {"passed": passed, "notes": notes}
        print(json.dumps(output, indent=2))
        sys.exit(0 if all(c[1] for c in checks) else 1)

    # Human-readable
    plugin_ver = manifest.get("version", "?") if manifest else "?"
    print(f"\n{BOLD}Composer v{plugin_ver} — Plugin Validator{RESET}")
    print(f"Root: {root}\n")

    for title, passed, notes in checks:
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"{BOLD}{title}{RESET}  [{status}]")
        for note in notes:
            print(f"  {note}")
        print()
        if not passed:
            all_pass = False

    # Summary
    total  = len(checks)
    passed = sum(1 for _, p, _ in checks if p)
    failed = total - passed

    print("─" * 50)
    if all_pass:
        print(f"{GREEN}{BOLD}All checks passed ({passed}/{total}).{RESET}")
        print("Run /compose with any brief to get started.")
    else:
        print(f"{RED}{BOLD}{failed} check(s) failed ({passed}/{total} passed).{RESET}")
        print("Fix the issues above, then re-run: python3 validate.py")
    print()

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a Composer plugin installation.")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()
    run_checks(as_json=args.json)
