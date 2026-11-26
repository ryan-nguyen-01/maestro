# R-030: Learning Loop (study before building, retro after, prevention over resolution)

## Applies to

Task Analysis and every producing agent (study and pre-flight), Coordinator (retro trigger), Memory
Update (promotion), Dev Verification and QC (prevention checks). Extends R-010 memory rules.

## Purpose

A team gets better because it studies before it builds and turns every mistake into something that
makes the mistake impossible next time. Maestro does the same, on the record: study notes before
unfamiliar work, a retro after meaningful work, and a promotion ladder that turns repeated lessons into
enforced project conventions and, when they generalize, into proposals for the house standards.

## Before the work

```text
R-030-01: STUDY BEFORE BUILD. When a task touches a technology, domain, or code area with no knowledge
  entry, or the agent's confidence about how to do it well is below high, it runs a time-boxed study
  first, in this order: (1) code in this repo that already does something similar — the house pattern
  to follow; (2) the matching skill; (3) official documentation when the adapter can reach it. It
  records a short study note in the task journal: sources, key constraints, the pattern chosen and why.
  Never write against an API, library signature, or config format from memory when the source can be
  checked. Durable findings go to knowledge through Memory Update.
R-030-02: PRE-FLIGHT LESSONS. Task Analysis pulls the anti-patterns, project conventions (PC-<n>), and
  bug patterns that match the touched components and tech into the task's critical checks /
  dev_verification_checklist, so known mistakes are checked before they can recur (R-007-15).
```

## After the work

```text
R-030-03: RETRO ON CLOSE. Write .maestro/work/tasks/<task-id>/retro.md (retro.template.md) when:
  a governed or autonomous task reaches DONE, is cancelled, or escalates at a hard-stop; or an
  assisted task needed at least one rework loop. Direct tasks write one journal line only when
  something went wrong. The retro records: what went well, what went wrong (with evidence), the root
  cause traced to a process or knowledge gap (5 whys — "the model made a mistake" is not a root cause),
  the prevention, the quality signals (R-030-07), and promotion candidates.
R-030-04: PROMOTION LADDER (owner: Memory Update, extends R-010-09..14):
    observation  first occurrence              -> .maestro/memory/project/feedback/inbox.md
    pattern      recurs >= 2x, or 1 severe      -> patterns.md / anti-patterns.md with root_cause,
                                                   prevention_rule, regression_check, recurrence_key
    convention   a pattern that applies to every -> .maestro/knowledge/conventions.md as PC-<n>; enforced
                 change in this project            in reviews exactly like a standard id (R-029-03)
    proposal     the lesson would apply to any   -> .maestro/memory/project/feedback/standard-proposals.md
                 project, not just this one        (R-030-05)
R-030-05: STANDARD PROPOSALS. A proposal states the proposed id and text, the level, the evidence
  (>= 2 incidents or 1 severe, with task/bug ids), and the prevention it enables. Proposals change
  .maestro/engine/standards/ only through user-approved framework maintenance (R-025-11, R-029-08).
R-030-06: PREVENTION OVER RESOLUTION. A lesson counts as learned only when it exists as something
  checkable: a test, a lint or type rule, a hook, a template field, or a checklist item with an id.
  "Be more careful next time" is not a prevention and is rejected by Memory Update.
R-030-07: QUALITY SIGNALS. Each retro records, when measurable: MUST findings at first review (first-
  pass yield), rework loops per stage, bugs found by QC after DEV_DONE (escaped to QC), challenges
  raised and accepted (R-028). Memory Update keeps the trend in knowledge so the loop can show whether
  it works. Unknown is recorded as unknown — never estimated to look good.
R-030-08: RETIRE STALE LESSONS. When the code or decision a convention/pattern guards no longer exists,
  Memory Update retires it with a note instead of leaving it to mislead future work.
```

## Evidence

```text
- study note in journal.md for unfamiliar work (sources cited)
- retro.md for qualifying tasks; promotions recorded in memory-updates.yaml
- every promoted entry carries a checkable prevention (R-030-06)
```

## Violation handling

A retro without a root cause or prevention is returned to its author. A lesson that recurs after being
recorded without a prevention is escalated to Memory Update for a stronger prevention and noted in the
next retro.
