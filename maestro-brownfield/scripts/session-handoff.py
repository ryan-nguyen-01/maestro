#!/usr/bin/env python3
"""Read and write `.maestro/runtime/session-handoff.yaml` without third-party packages.

The adapter-neutral continuation pointer (R-027). Any harness — Claude Code, Codex CLI,
Cursor, Copilot — resumes from the same brief and writes the same file at phase boundaries.

  python3 scripts/session-handoff.py --show
  python3 scripts/session-handoff.py --check
  python3 scripts/session-handoff.py --adapter codex --state IN_DEV --task TASK-... \
      --step "coder-leader assigned auth + api" --next /dev --owner coder-leader \
      --read .maestro/work/tasks/TASK-.../implementation-plan.yaml
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".maestro" / "runtime"
HANDOFF = RUNTIME / "session-handoff.yaml"
STATE = RUNTIME / "workflow-state.yaml"
ADAPTERS = ("claude", "codex", "cursor", "copilot", "other")


def activity_module() -> Any:
    """Reuse the dependency-free YAML load/dump/secret helpers already shipped in scripts/."""
    module_path = ROOT / "scripts" / "agent-activity.py"
    spec = importlib.util.spec_from_file_location("agent_activity", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_ACTIVITY = None


def activity() -> Any:
    global _ACTIVITY
    if _ACTIVITY is None:
        _ACTIVITY = activity_module()
    return _ACTIVITY


def load_yaml(path: Path) -> dict[str, Any]:
    data = activity().load_yaml(path)
    return data if isinstance(data, dict) else {}


def seed() -> dict[str, Any]:
    now = activity().now_utc()
    return {
        "schema_version": "1.0",
        "role": "session-handoff",
        "adapter": {"last": "other", "session_started_at": now, "updated_at": now},
        "position": {
            "current_state": "NEW",
            "active_task_id": None,
            "active_subtask_id": None,
            "active_run_id": None,
            "active_checkpoint_id": None,
            "execution_mode": None,
            "target_scope": None,
        },
        "progress": {
            "last_completed_step": None,
            "last_artifact": None,
            "next_command": "/coord",
            "next_owner_agent": "coordinator",
            "blocked": False,
            "blocker": None,
        },
        "read_next": [],
        "open_questions": [],
        "do_not_reopen": [],
    }


def ensure(data: dict[str, Any]) -> dict[str, Any]:
    base = seed()
    for key, default in base.items():
        value = data.get(key, default)
        if isinstance(default, dict):
            merged = dict(default)
            if isinstance(value, dict):
                merged.update({k: v for k, v in value.items() if k in default})
            data[key] = merged
        elif isinstance(default, list):
            data[key] = value if isinstance(value, list) else []
        else:
            data[key] = value
    return data


def reconcile(data: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """workflow-state.yaml is authoritative (R-027-02); return the corrections applied."""
    if not state:
        return []
    corrections: list[str] = []
    mapping = {
        "current_state": "current_state",
        "active_task_id": "active_task_id",
        "active_subtask_id": "active_subtask_id",
        "active_run_id": "active_run_id",
        "active_checkpoint_id": "active_checkpoint_id",
    }
    for pos_key, state_key in mapping.items():
        if state_key not in state:
            continue
        authoritative = state.get(state_key)
        if data["position"].get(pos_key) != authoritative:
            corrections.append(f"position.{pos_key}: {data['position'].get(pos_key)!r} -> {authoritative!r}")
            data["position"][pos_key] = authoritative
    mode = state.get("active_execution_mode") or state.get("default_execution_mode")
    if mode and data["position"].get("execution_mode") != mode:
        corrections.append(f"position.execution_mode: {data['position'].get('execution_mode')!r} -> {mode!r}")
        data["position"]["execution_mode"] = mode
    return corrections


def fmt(value: Any, default: str = "none") -> str:
    return default if value is None or value == "" else str(value)


def render(data: dict[str, Any], corrections: list[str], state_exists: bool) -> str:
    pos, prog = data["position"], data["progress"]
    lines = [
        "Resume Brief",
        "============",
        f"prev adapter : {fmt(data['adapter'].get('last'))} (updated {fmt(data['adapter'].get('updated_at'), 'unknown')})",
        f"state        : {fmt(pos.get('current_state'), 'NEW')}"
        f" | mode {fmt(pos.get('execution_mode'), '-')}"
        f" | scope {fmt(pos.get('target_scope'), '-')}",
        f"task / run   : {fmt(pos.get('active_task_id'))} / {fmt(pos.get('active_run_id'))}",
        f"last step    : {fmt(prog.get('last_completed_step'), '-')}",
        f"last artifact: {fmt(prog.get('last_artifact'), '-')}",
        f"next         : {fmt(prog.get('next_command'), '/coord')} (owner: {fmt(prog.get('next_owner_agent'), 'coordinator')})",
    ]
    if prog.get("blocked"):
        lines.append(f"BLOCKED      : {fmt(prog.get('blocker'), 'reason not recorded')}")
    read_next = data.get("read_next") or []
    lines.append("read next    :" + (" (none recorded — start from workflow.md)" if not read_next else ""))
    lines.extend(f"  {i}. {p}" for i, p in enumerate(read_next, 1))
    for label, key in (("open questions", "open_questions"), ("do not reopen", "do_not_reopen")):
        items = data.get(key) or []
        if items:
            lines.append(f"{label}:")
            lines.extend(f"  - {item}" for item in items)
    if not state_exists:
        lines.append("")
        lines.append("note: .maestro/runtime/workflow-state.yaml is absent — treat state as NEW and route to /coord.")
    if corrections:
        lines.append("")
        lines.append("drift corrected against workflow-state.yaml (authoritative):")
        lines.extend(f"  - {c}" for c in corrections)
    return "\n".join(lines)


def apply_updates(data: dict[str, Any], args: argparse.Namespace) -> bool:
    act = activity()
    fields: list[tuple[str, str, Any]] = [
        ("position", "current_state", args.state),
        ("position", "active_task_id", args.task),
        ("position", "active_subtask_id", args.subtask),
        ("position", "active_run_id", args.run),
        ("position", "active_checkpoint_id", args.checkpoint),
        ("position", "execution_mode", args.mode),
        ("position", "target_scope", args.scope),
        ("progress", "last_completed_step", args.step),
        ("progress", "last_artifact", args.artifact),
        ("progress", "next_command", args.next),
        ("progress", "next_owner_agent", args.owner),
        ("progress", "blocker", args.blocker),
    ]
    touched = False
    for section, key, value in fields:
        if value is None:
            continue
        act.reject_unsafe_text(f"{section}.{key}", value)
        data[section][key] = value
        touched = True
    if args.adapter:
        data["adapter"]["last"] = args.adapter
        touched = True
    if args.read is not None:
        act.reject_unsafe_text("read_next", args.read)
        data["read_next"] = args.read
        touched = True
    if args.open_question is not None:
        act.reject_unsafe_text("open_questions", args.open_question)
        data["open_questions"] = args.open_question
        touched = True
    if args.blocked is not None:
        data["progress"]["blocked"] = args.blocked
        touched = True
    return touched


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Read/write the adapter-neutral session handoff (R-027).")
    p.add_argument("--show", action="store_true", help="Print the resume brief (default action).")
    p.add_argument("--json", action="store_true", help="Print the handoff as JSON.")
    p.add_argument("--check", action="store_true", help="Exit non-zero when the pointer drifted from workflow-state.yaml.")
    p.add_argument("--adapter", choices=ADAPTERS, help="Adapter taking over this session.")
    p.add_argument("--state", help="Workflow state to record (must match workflow-state.yaml).")
    p.add_argument("--task", help="Active task id.")
    p.add_argument("--subtask", help="Active subtask id.")
    p.add_argument("--run", help="Active run id.")
    p.add_argument("--checkpoint", help="Active checkpoint id.")
    p.add_argument("--mode", choices=["direct", "assisted", "governed"], help="Execution mode.")
    p.add_argument("--scope", choices=["framework", "product_component", "unknown"], help="Target scope.")
    p.add_argument("--step", help="Short sentence: what was just completed.")
    p.add_argument("--artifact", help="Path to the artifact proving the completed step.")
    p.add_argument("--next", help="Next command, e.g. /dev.")
    p.add_argument("--owner", help="Agent that owns the next command.")
    p.add_argument("--read", nargs="*", help="Ordered minimal read list for the next session.")
    p.add_argument("--open-question", nargs="*", dest="open_question", help="Unresolved questions for the next session.")
    p.add_argument("--blocked", dest="blocked", action="store_true", default=None, help="Mark the pointer blocked.")
    p.add_argument("--unblocked", dest="blocked", action="store_false", help="Clear the blocked flag.")
    p.add_argument("--blocker", help="Blocker description.")
    return p


def main() -> int:
    args = build_parser().parse_args()
    state = load_yaml(STATE)
    data = ensure(load_yaml(HANDOFF))
    corrections = reconcile(data, state)
    warnings: list[str] = []

    if apply_updates(data, args):
        authoritative_state = state.get("current_state")
        if args.state and authoritative_state and args.state != authoritative_state:
            warnings.append(
                f"recorded state {args.state!r} contradicts workflow-state.yaml {authoritative_state!r};"
                " update workflow-state.yaml too or the next session will be corrected back (R-027-02)."
            )
        # An explicit write is this session's intent; do not re-apply the drift it just overrode.
        corrections = []
        now = activity().now_utc()
        data["adapter"]["updated_at"] = now
        if args.adapter:
            data["adapter"]["session_started_at"] = now
        activity().write_yaml(HANDOFF, data)
    elif corrections and HANDOFF.exists():
        # R-027-02: the pointer is rewritten to match the authoritative source, not left stale.
        activity().write_yaml(HANDOFF, data)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 1 if args.check and corrections else 0
    print(render(data, corrections, STATE.exists()))
    for warning in warnings:
        print(f"warning: {warning}")
    if args.check and corrections:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
