# `.claude/` — Definitions

`.claude/` holds what the workspace **is**: agent definitions, skills, slash commands, the engine
(workflow, rules, house standards, templates, docs, contracts), harness settings, and the manifest.
It changes only during user-approved framework maintenance (R-025-11). Everything the agents **write
while working** lives in [`.maestro/`](../.maestro/README.md).

Why the split: Claude Code treats `.claude/` as a protected directory — Write/Edit there needs a per-call
approval and permission allow-rules do not lift it (verified with Claude Code 2.1.287). Runtime state
inside `.claude/` would stall every workflow step; definitions inside `.claude/` get write protection for
free.

```text
.claude/
├── INSTRUCTIONS.md       Stable harness entry point (read order)
├── README.md             This file
├── manifest.yaml         Ownership, writable boundary, optional domains
├── settings.json         Harness permissions and hooks (personal overrides: settings.local.json, git-ignored)
├── agents/               Flat agent definitions (`<name>.agent.md`, no subfolders)
├── commands/             Slash-command contracts
├── skills/               Flat skill collection (`<name>/SKILL.md`)
└── engine/               Canonical control plane: workflow, rules, standards, templates, docs, contracts
```

`agents/` and `skills/` are intentionally **flat** so every harness (Claude Code, Codex, Copilot,
Cursor, …) can discover them without folder conventions. Do not store secrets, credentials, private
data, or long logs anywhere under `.claude/`.
