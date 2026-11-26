#!/usr/bin/env python3
"""Workspace self-test: catches the defects the architecture health check cannot see.

  links    relative markdown links that do not resolve
  paths    references to a control-plane domain (.maestro/<x>, .claude/<x>) that does not exist and is
           not declared optional in the manifest (pruned folders, moved folders, typos)
  hooks    the PreToolUse guard scripts block what they must and allow framework/state writes
  scripts  the health check, status dashboard, and catalog checks run cleanly
  copy     (--template only) the folder is clean to copy as a new workspace: no junk (.agent/, .DS_Store,
           __pycache__), no leftover state (runtime files, session memory, task folders), no absolute
           machine paths

Usage:  python3 scripts/selftest.py              # a live workspace: exit 1 when anything fails
        python3 scripts/selftest.py --template   # a template about to be copied: adds the copy checks
        python3 scripts/selftest.py --verbose    # list every finding
No third-party dependencies. Safe to run anytime: it reads files and runs hooks with synthetic payloads.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"skills", "marketplace", "node_modules", ".git", "__pycache__", "reports", "history"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".json", ".toml"}
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PATH_RE = re.compile(r"(?<![\w/.-])(\.(?:maestro|claude|codex)/[A-Za-z0-9_./-]*[A-Za-z0-9_/-])")
# Mentions that are intentionally not paths in this workspace ("do not use .claude/rules", legacy paths).
INTENTIONAL = {".claude/rules", ".claude/control-plane", ".maestro/control-plane"}


def text_files():
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in TEXT_SUFFIXES and not SKIP_PARTS.intersection(p.relative_to(ROOT).parts):
            yield p


def check_links() -> list[str]:
    bad = []
    for f in text_files():
        if f.suffix != ".md":
            continue
        text = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8", errors="ignore"), flags=re.S)
        for target in LINK_RE.findall(text):
            if re.match(r"^(https?:|mailto:|#|<|\{)", target) or "{{" in target or "<" in target:
                continue
            path = target.split("#")[0]
            if path and not (f.parent / path).resolve().exists():
                bad.append(f"{f.relative_to(ROOT)} -> {target}")
    return bad


def optional_domains() -> set[str]:
    for m in (ROOT / ".maestro/manifest.yaml", ROOT / ".claude/manifest.yaml"):
        if m.exists():
            text = m.read_text(encoding="utf-8")
            if "optional_domains:" in text:
                return set(re.findall(r'^\s+- "([^"]+)"', text.split("optional_domains:", 1)[1], re.M))
    return set()


def check_paths() -> list[str]:
    bad: set[str] = set()
    optional = optional_domains()
    for f in text_files():
        for ref in PATH_RE.findall(f.read_text(encoding="utf-8", errors="ignore")):
            if any(c in ref for c in "<{*") or ref.endswith("/."):
                continue
            ref = re.sub(r"(\.(?:ya?ml|md|json))\..*$", r"\1", ref.rstrip("."))  # project.yaml.product -> file
            parts = Path(ref).parts
            if "/".join(parts[:2]) in INTENTIONAL or any(ref == o or ref.startswith(o + "/") for o in optional):
                continue
            if ROOT.joinpath(*parts[:2]).exists():
                continue  # domain exists; deeper files may be created at runtime
            if len(parts) == 2 and "." in parts[1] and (ROOT / parts[0]).exists():
                continue  # a local file directly under an existing control-plane dir
            bad.add(f"{'/'.join(parts[:2])}  (first seen in {f.relative_to(ROOT)})")
    return sorted(bad)


def state_dir() -> str:
    return ".maestro" if (ROOT / ".maestro" / "runtime").is_dir() else ".claude"


def run_hook(hook: str, payload: dict) -> int:
    script = ROOT / "scripts" / "hooks" / f"{hook}.py"
    if not script.exists():
        return -1
    env = {k: v for k, v in os.environ.items() if k not in {"MAESTRO_HOOK_PROFILE", "MAESTRO_DISABLED_HOOKS"}}
    r = subprocess.run([sys.executable, str(script)], input=json.dumps({"cwd": str(ROOT), **payload}),
                       text=True, capture_output=True, cwd=ROOT, env=env)
    return r.returncode


def check_hooks() -> list[str]:
    sd = state_dir()
    secret = "API_KEY = 'sk-" + "a1b2c3d4e5f6g7h8i9j0k1l2m3'\n"  # split so this file never trips the guard
    cases = [
        ("secret-guard", "Write", {"file_path": str(ROOT / "notes.py"), "content": secret}, 2, "blocks a secret"),
        ("secret-guard", "Write", {"file_path": str(ROOT / "notes.md"), "content": "hello\n"}, 0, "allows plain text"),
        ("destructive-guard", "Bash", {"command": "rm -rf /"}, 2, "blocks rm -rf /"),
        ("destructive-guard", "Bash", {"command": "git push --force origin main"}, 2, "blocks force push"),
        ("destructive-guard", "Bash", {"command": "ls -la && git status"}, 0, "allows read-only commands"),
        ("scope-guard", "Write", {"file_path": str(ROOT / sd / "work/tasks/T-1/journal.md"), "content": "x"}, 0,
         f"allows state writes ({sd}/work)"),
        ("scope-guard", "Write", {"file_path": str(ROOT / sd / "work/tasks/T-1/tests/plan.md"), "content": "x"}, 0,
         f"allows state paths containing a source token ({sd}/work/.../tests/)"),
        ("scope-guard", "Write", {"file_path": str(ROOT / ".claude/skills/x/lib/y.md"), "content": "x"}, 0,
         "allows framework paths containing a source token (.claude/skills/<x>/lib/)"),
    ]
    fails = []
    for hook, tool, tool_input, want, label in cases:
        got = run_hook(hook, {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input})
        if got not in (-1, want):
            fails.append(f"{hook}: {label}: exit {got}, want {want}")
    return fails


def check_scripts() -> list[str]:
    cmds = [["scripts/architecture-health-check.py", "--strict"]]
    cmds += [["scripts/status-dashboard.py", "--mode", m] for m in ("compact", "dashboard", "models", "json")]
    cmds += [["scripts/build-skill-catalog.py", "--check"], ["scripts/session-handoff.py", "--help"]]
    fails = []
    for c in cmds:
        if not (ROOT / c[0]).exists():
            continue
        r = subprocess.run([sys.executable, *c], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            tail = ((r.stdout + r.stderr).strip().splitlines() or [""])[-1]
            fails.append(f"{' '.join(c)} -> exit {r.returncode}: {tail[:160]}")
    return fails


def check_copy_ready() -> list[str]:
    """A template must contain nothing that belongs to one particular machine, session, or project."""
    bad = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if p.name in {".agent", "__pycache__", ".DS_Store"} or p.suffix == ".pyc":
            bad.append(f"junk: {rel}")
    sd = ROOT / state_dir()
    allowed = {"README.md", ".gitkeep", "index.yaml"}
    for sub in ("runtime", "memory/sessions"):
        for f in (sd / sub).rglob("*") if (sd / sub).is_dir() else []:
            if f.is_file() and f.name not in allowed and "cache" not in f.relative_to(sd).parts:
                bad.append(f"leftover state: {f.relative_to(ROOT)}")
    for sub in ("work/tasks", "work/bugs", "work/runs", "memory/tasks"):
        d = sd / sub
        for child in (d.iterdir() if d.is_dir() else []):
            content = [f for f in child.rglob("*") if f.is_file() and f.name not in allowed] if child.is_dir() else []
            if content:  # skeleton folders holding only README/.gitkeep are part of the template
                bad.append(f"leftover work: {child.relative_to(ROOT)} ({len(content)} files)")
    tmp_dirs = "|".join(re.escape(x) for x in ("/private" + "/tmp/", "/var" + "/folders/"))  # split: no self-match
    machine = re.compile(r"/(?:Users|home)/(?!user\b|you\b|me\b|<)[A-Za-z0-9._-]+/|" + tmp_dirs)
    for f in text_files():
        m = machine.search(f.read_text(encoding="utf-8", errors="ignore"))
        if m:
            bad.append(f"machine path {m.group(0)!r} in {f.relative_to(ROOT)}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--template", action="store_true", help="also check the folder is clean to copy")
    args = ap.parse_args()
    results = {"links": check_links(), "paths": check_paths(), "hooks": check_hooks(), "scripts": check_scripts()}
    if args.template:
        results["copy"] = check_copy_ready()
    total = sum(len(v) for v in results.values())
    print(f"selftest {ROOT.name}: " + " ".join(f"{k}={len(v)}" for k, v in results.items()) +
          f" -> {'PASS' if total == 0 else 'FAIL'}")
    for k, v in results.items():
        for item in (v if args.verbose else v[:5]):
            print(f"  [{k}] {item}")
        if not args.verbose and len(v) > 5:
            print(f"  [{k}] ... +{len(v) - 5} more (--verbose)")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
