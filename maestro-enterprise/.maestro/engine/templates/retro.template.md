---
task_id: "{{TASK_ID}}"
closed_as: "done|cancelled|hard-stop|rework"
written_by: "{{AGENT}}"
written_at: "{{ISO8601}}"
---

# Retro — {{TASK_TITLE}}

> R-030-03. Blameless and evidence-based. Every "went wrong" item ends in a checkable prevention.

## Outcome

One paragraph: what was delivered against the acceptance criteria, with links to the evidence.

## Went well (keep doing)

- <practice> — evidence: <artifact / command / review id>

## Went wrong

| # | What happened | Evidence | Root cause (5 whys, process/knowledge gap) | Prevention (checkable) | Type |
| - | --- | --- | --- | --- | --- |
| 1 | | | | | test / lint / hook / template / checklist id |

"The model made a mistake" and "be more careful" are not accepted (R-030-03, R-030-06).

## Challenges

| Id | Raised by | Severity | Accepted? | Was the challenge right in hindsight? |
| --- | --- | --- | --- | --- |

## Quality signals (R-030-07 — unknown stays unknown)

```yaml
first_pass_must_findings: unknown     # MUST findings at the first code/design review
rework_loops: { analysis: 0, dev: 0, qc: 0 }
escaped_to_qc: unknown                # bugs QC found after DEV_DONE
challenges: { raised: 0, accepted: 0 }
```

## Promotions (R-030-04)

| Lesson | Occurrences | Promote to | Entry id |
| --- | --- | --- | --- |
| | | inbox / pattern / anti-pattern / convention PC-n / standard proposal | |
