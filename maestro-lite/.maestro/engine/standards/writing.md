# Writing Standard (WS)

The house bar for every document Maestro produces: specs, ADRs, analyses, handoffs, QC reports, status
updates, and the final handover. Levels and precedence: [README.md](README.md). Document shapes come from
`.maestro/engine/templates/` and the BA documentation standard; this file governs how they read.

```text
WS-01 MUST   Bottom line up front. The first paragraph states the conclusion, decision, or ask. Background
             comes after, for readers who need it.
WS-02 MUST   Write for a named reader (the user, the next agent, a reviewer) and say what they should do
             after reading. Match depth to that reader, not to the author's effort.
WS-03 MUST   Claims carry sources (file:line, document id, command, test run — R-024-04). Numbers carry
             units and an as-of date when they can change.
WS-04 MUST   Honest vocabulary: no "should work", "mostly done", "probably fine", "seems to". Status is
             done-with-evidence, blocked-because-X, or in-progress-remaining-Y (R-025-05).
WS-05 SHOULD One idea per paragraph; short sentences; active voice; concrete nouns over abstractions.
WS-06 SHOULD Built for scanning: headings that state the point, lists for parallel items, tables for
             comparisons, code blocks for anything copy-pasteable.
WS-07 MUST   Decisions record context, options considered, the decision, its consequences, and who decided
             (ADR shape) — including the dissent when someone disagreed and committed (R-028-04).
WS-08 MUST   Acceptance criteria are Given/When/Then, testable, one behavior each, with ids (R-022).
WS-09 SHOULD Delete before adding: an update removes what it makes obsolete. One source per fact; link
             rather than copy (R-018).
WS-10 MUST   Language follows the language policy: artifacts in English unless the project sets
             otherwise; replies to the user in the user's language.
WS-11 SHOULD Handover and final reports use: Done (with evidence) / Decisions and assumptions / Risks and
             open items / How to run or verify / Next step.
WS-12 SHOULD Assumptions are visible and labeled with confidence, not buried in prose.
```

## Before sending any document

```text
[ ] Could the reader act on the first paragraph alone? (WS-01)
[ ] Every claim sourced or labeled as an assumption with confidence (WS-03, WS-12)
[ ] No forbidden status vocabulary (WS-04)
[ ] Anything obsolete removed; nothing duplicated from another source of truth (WS-09)
```
