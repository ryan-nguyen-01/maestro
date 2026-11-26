# Maestro SDLC

Classic software delivery: web, mobile, API products built greenfield through the full BA -> design -> UI/UX -> code -> QC pipeline.

## Quick start — copy, add your information, talk

1. **Copy** this folder anywhere and name it after your project: `cp -R maestro-sdlc ~/work/my-app`
2. **Add your information** — only what you have; nothing is required:

| What you have | Put it in |
| --- | --- |
| Just an idea | Nothing to copy — describe it in the chat. Maestro drafts a blueprint and a clickable UI prototype and asks you to approve it before any code. |
| Documents: PRD, specs, user stories, API contracts, designs, glossary | `inputs/` (agents read it, never edit it; facts are cited back to the file) |
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
