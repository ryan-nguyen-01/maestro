# Maestro ADLC

Agent Development Lifecycle: building agentic products — agents with a mission, tools, memory, and a
planning loop — with a behavior eval gate before done.

## Quick start — copy, add your information, talk

1. **Copy** this folder anywhere and name it after your project: `cp -R maestro-adlc ~/work/my-agent`
2. **Add your information** — only what you have; nothing is required:

| What you have | Put it in |
| --- | --- |
| Just an idea for an agent | Nothing to copy — describe it in the chat. Maestro drafts a blueprint (mission, tools, memory, eval plan) and asks you to approve it before any code. |
| Documents: PRD, requirements, API contracts, designs | `docs/product/`, `docs/requirements/`, `docs/architecture/` — or paste the text into the chat |
| Existing agents / prompts | `agents/<agent-name>/` (`agent.md`, `tools.yaml`, `prompts/`) |
| Example conversations, golden answers, test datasets | `evals/<agent-name>/` |
| An existing host app (API / UI) | `app/` |
| Product name / identity | Nothing — Maestro proposes it during onboarding and writes `.maestro/project.yaml` only after you confirm |
| Secrets (API keys, passwords) | Never in this folder — keep them in your local `.env`; Maestro asks when a step needs one |

3. **Run** `claude` (or `codex`) inside the folder and just talk — "bạn là ai", "xây cho tôi agent ...",
   "thêm tool cho agent X", "tình hình?". No commands needed; shortcuts are in COMMAND.md.

`.claude/` holds the definitions (agents, skills, commands, engine) and `.maestro/` holds everything
Maestro writes while working. Check the folder anytime: `python3 scripts/selftest.py`.

A self-contained Maestro workspace with an agent-native folder tree: `agents/` for the agents you
build (one folder per agent: `agent.md` mission, `tools.yaml` contracts, `prompts/` versioned,
`memory.yaml`, `knowledge/`), `evals/` for behavior eval suites (the eval gate: task success,
trajectory, tool-call, safety), `app/` for the host application that serves the agents, and `tests/`.
Copy this folder anywhere, put your agents in `agents/` and the host app in `app/` (register paths in
`.maestro/registry/components.yaml`),
then run `claude` (or `codex`) in this folder and JUST DESCRIBE what you want in plain language
("xây cho tôi agent ...", "thêm tool cho agent X", "tình hình?") — no commands needed; the coordinator
maps intent to the right flow. Power-user shortcuts exist in COMMAND.md if you want them.

Entry points: `AGENTS.md` (shared instructions for every tool) - `CLAUDE.md` (imports `AGENTS.md`
+ Claude Code specifics) - `COMMAND.md` (commands) - `.claude/INSTRUCTIONS.md` (control-plane read order).
Validated against Claude Code 2.1.287 (`claude plugin validate` on agents, skills, commands); the
`@AGENTS.md` import works on every version.

A self-contained workspace — edit it directly (see VARIANT.yaml). The folder tree is fit to developing
agents: agent definitions in `agents/`, behavior eval suites in `evals/`, host app in `app/`, product
docs in `docs/`.
