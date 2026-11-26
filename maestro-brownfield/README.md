# Maestro Brownfield

Maintain an EXISTING, running project: deep onboarding first, execute assigned tasks precisely, ask when unclear — never infer.

## Quick start — copy, add your information, talk

1. **Copy** this folder anywhere and name it after your project: `cp -R maestro-brownfield ~/work/my-app-ws`
2. **Add your information** — only what you have:

| What you have | Put it in |
| --- | --- |
| The existing project's code | `source/<service-or-app>/` — one folder per service, app, or package (keep its own git history if you like) |
| Specs, bug reports, error logs, screenshots, data dumps | `intake/` — anything goes; Maestro triages it first and never quotes secrets it finds |
| A brand-new idea (no existing code) | Use `maestro-sdlc` or `maestro-lite` instead — this template maintains existing projects |
| Product name / identity | Nothing — Maestro proposes it during onboarding and writes `.maestro/project.yaml` only after you confirm |
| Secrets (API keys, passwords) | Never in this folder — keep them in your local `.env`; Maestro asks when a step needs one |

3. **Run** `claude` (or `codex`) inside the folder and just talk — "phân tích dự án này" first, then
   "sửa bug trong intake/...", "thêm tính năng X", "tình hình?". Maestro asks whenever something is
   unclear instead of guessing (ask-don't-infer).

`.claude/` holds the definitions (agents, skills, commands, engine) and `.maestro/` holds everything
Maestro writes while working. Check the folder anytime: `python3 scripts/selftest.py`.

A self-contained Maestro workspace with a purpose-fit folder tree: `source/` for the existing
project's code (one folder per service/app/package) and `intake/` for raw material you drop in
(specs, bug reports, error logs, dumps). Copy this folder anywhere, move your project into `source/`,
drop any material into `intake/`,
then run `claude` (or `codex`) in this folder and JUST DESCRIBE what you want in plain language
("phân tích dự án này", "sửa bug X", "tình hình?") — no commands needed; the coordinator maps
intent to the right flow. Power-user shortcuts exist in COMMAND.md if you want them.

Entry points: `CLAUDE.md` (Claude) - `AGENTS.md` (Codex) - `COMMAND.md` (commands)
- `.claude/INSTRUCTIONS.md` (workflow brain).

A self-contained workspace — edit it directly (see VARIANT.yaml). The folder tree is fit to
maintenance work: code in `source/`, raw user material in `intake/`.
