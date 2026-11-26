# Maestro Lite

Lightweight bundle for small tools, scripts, and prototypes: fast, minimal ceremony, still safe.

## Quick start — copy, add your information, talk

1. **Copy** this folder anywhere and name it after your project: `cp -R maestro-lite ~/work/my-app`
2. **Add your information** — only what you have; nothing is required:

| What you have | Put it in |
| --- | --- |
| Just an idea | Nothing to copy — describe it in the chat. Maestro confirms a 5-line mini-brief (what, stack, done-when) and builds. |
| Documents: PRD, specs, user stories, API contracts, designs, glossary | `docs/` — or paste the text into the chat |
| Existing code | `apps/` (web, mobile, CLI) · `services/` (backends, workers) · `packages/` (shared libraries) |
| Product name / identity | Nothing — Maestro proposes it during onboarding and writes `.maestro/project.yaml` only after you confirm |
| Secrets (API keys, passwords) | Never in this folder — keep them in your local `.env`; Maestro asks when a step needs one |

3. **Run** `claude` (or `codex`) inside the folder and just talk — "bạn là ai", "phân tích dự án này", "build cho tôi app ...", "sửa bug X", "tình hình?". No commands needed; shortcuts are in COMMAND.md.

## What is in the folder

```text
.claude/    definitions: agents, skills, commands, settings — Maestro does not edit these while working
.maestro/   engine + workspace state: everything Maestro writes while working (runtime/ stays local)
docs/       official product documents Maestro produces (requirements, design, architecture, QC)
```

Entry points: `CLAUDE.md` (Claude) · `AGENTS.md` (Codex) · `COMMAND.md` (commands) · `.maestro/INSTRUCTIONS.md` (workflow brain). Check the folder anytime: `python3 scripts/selftest.py`.

Generated from the maestro platform — do not edit framework files by hand (see VARIANT.yaml).
