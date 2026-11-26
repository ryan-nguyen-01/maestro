# Code Standard (CS)

The house bar for every line of product code Maestro writes or reviews. Language idioms come from the
matching skill (`.claude/skills/<stack>/SKILL.md`) and the project's conventions; this file is the
language-independent floor and default. Levels and precedence: [README.md](README.md).

## A. Shape of the change

```text
CS-01 MUST   One change, one purpose. The diff is explainable in two sentences tied to its purpose_ref.
             Unrelated refactors, renames, and "while I'm here" fixes go to their own task (R-024-05).
CS-02 MUST   Respect the component's layering: no business rules in controllers, handlers, or UI
             components; no data access from the presentation layer; no cross-module reach into another
             module's internals or tables. Each new file has an obvious home layer.
CS-03 SHOULD No speculative generality: no interface with one implementation, config flag nobody sets,
             plugin point without a second plugin, or generic helper with one caller — unless an
             acceptance criterion or ADR requires it.
CS-04 SHOULD Reuse before writing: search for an existing helper, component, hook, or util first. A new
             near-duplicate of existing code is a review finding.
CS-05 MUST   A new dependency is justified in the journal or ADR: what it does that the stdlib and the
             existing dependencies cannot, maintenance health, license, size, and known vulnerabilities.
```

## B. Naming and readability

```text
CS-06 MUST   Names reveal intent in the domain's vocabulary (glossary/BRD terms, not invented synonyms).
             Functions are verbs, types are nouns, booleans read as predicates (isExpired, hasAccess).
             No abbreviations beyond the universal (id, url, http, db).
CS-07 SHOULD A function does one thing at one level of abstraction. Aim for <= 40 lines and <= 3 levels
             of nesting; use guard clauses and early returns instead of deep if/else pyramids.
CS-08 SHOULD <= 4 parameters; beyond that pass a typed options object. No boolean parameter that switches
             behavior — split into two well-named functions.
CS-09 MUST   No magic values. Numbers and strings with business meaning (limits, timeouts, statuses,
             roles, URLs) are named constants or configuration.
CS-10 SHOULD Comments say WHY — constraints, trade-offs, links to an ADR or ticket — never restate WHAT
             the code says. No commented-out code. Every TODO carries a task id.
```

## C. Correctness and errors

```text
CS-11 MUST (floor) Never swallow an error. No empty catch; no catch-log-continue on a path whose caller
             needs to know. Handle it meaningfully, or propagate it with context.
CS-12 MUST   Errors carry context (operation, entity ids — never secrets or PII) and are mapped to the
             documented error catalog / status code at the boundary. Stack traces and internal details
             never reach end users.
CS-13 MUST (floor) Validate every external input at the trust boundary (API, queue, file, env, user,
             LLM output) against a schema. Inside the boundary, code works with typed, already-valid data.
CS-14 MUST   Handle edges explicitly: empty / null / zero / one / many / maximum, duplicates, unicode,
             time zones (store UTC, render local), money as integer minor units or a decimal type —
             never binary floating point.
CS-15 MUST   Anything that can be retried (webhooks, consumers, payments, client-retried POSTs) is
             idempotent or deduplicated. No check-then-act races on persisted data: use constraints,
             transactions, or conditional writes.
CS-16 MUST   Release every resource (connection, file, lock, subscription, timer) on every path including
             errors. Every network call has a timeout; retries are bounded, with backoff and jitter.
```

## D. Types and data

```text
CS-17 SHOULD Make illegal states unrepresentable: enums or unions over free strings, required fields not
             optional, parse into domain types at the boundary instead of re-validating everywhere.
CS-18 MUST   No any / unchecked casts / non-null assertions / @ts-ignore / type: ignore / unsafe blocks
             without an adjacent comment proving why it is safe.
CS-19 MUST   Schema changes ship with a migration that runs forward safely under live traffic. Breaking
             changes follow expand -> migrate -> contract; the rollback path is documented.
CS-20 SHOULD Immutable by default. Mutate only state you own, as locally as possible.
```

## E. Security (floor)

```text
CS-21 MUST (floor) No secrets in code, tests, fixtures, logs, or artifacts (R-013). Configuration comes
             from the environment or a secret manager; .env.example lists names, never values.
CS-22 MUST (floor) Parameterized queries or the ORM only. No string-built SQL, shell commands, HTML, or
             file paths from untrusted input. Encode output for its context.
CS-23 MUST (floor) Authorization is checked server-side on every protected operation, per resource
             (no IDOR). Deny by default; the client is never the enforcement point.
CS-24 MUST (floor) Logs and errors never contain passwords, tokens, full card numbers, or unmasked PII.
```

## F. Operability and performance

```text
CS-25 SHOULD Structured logs at boundaries with a correlation id. Levels mean something: error = a human
             must act; warn = degraded but handled; info = business events; debug = off in production.
CS-26 SHOULD A new user-facing or business-critical flow emits a metric or event so its health can be
             seen without reading logs.
CS-27 SHOULD No N+1 queries, no unbounded lists without pagination, an index for every new query
             pattern on large tables, no blocking I/O on an event loop or UI thread.
```

## G. Tests (when the test policy requires them)

```text
CS-28 MUST   Tests exercise the CHANGED behavior including at least one failure or edge path — not only
             the happy path that was already green (R-026-05).
CS-29 MUST   Tests are deterministic: no sleep-based synchronization, no uncontrolled network, clock, or
             randomness, no dependence on test order or shared mutable fixtures.
CS-30 SHOULD Test names state behavior ("rejects an expired token with 401"); one behavior per test;
             Arrange-Act-Assert; test the public contract, not private internals.
CS-31 MUST   A failing test is never deleted, skipped, or loosened to turn a build green unless that
             decision is recorded with the decision owner (R-000-12).
CS-32 SHOULD A bug fix starts with a test that reproduces the bug (red), then the fix (green).
```

## H. Finish

```text
CS-33 MUST   Change integrity (R-026): every caller updated, dead code removed, exactly one live path.
CS-34 MUST   Formatter, linter, type checker, and build are clean with zero NEW warnings. A suppression
             carries a reason next to it.
CS-35 MUST   Behavior, API, config, or env changes update their docs and contracts in the same change
             (README, OpenAPI/AsyncAPI, .env.example, changelog where the project keeps one).
CS-36 SHOULD Commits are atomic and their messages say why, not what (R-020).
```

## Review order

Review in this order and stop to send back early when a higher tier fails — polishing names on a change
with the wrong design wastes everyone's time:

```text
1. Purpose and design   Does this solve the acceptance criteria in the simplest way that fits the
                        architecture? (CS-01..05)
2. Correctness          Edges, errors, concurrency, resources, security floor. (CS-11..24)
3. Tests                Do they prove the changed behavior and fail when it breaks? (CS-28..32)
4. Readability          Would the next engineer understand it without the author? (CS-06..10, 17..20)
5. Finish               Integrity, clean build, docs. (CS-33..36)
```

Approve when the change clearly improves the health of the codebase and no MUST is open. Do not hold a
change hostage to perfection or to SHOULD items the author has justified.

## Author self-check before handoff (R-028-09)

```text
[ ] Could this be simpler and still meet every acceptance criterion?
[ ] What input, state, or timing breaks it? Did I handle or test that?
[ ] Which assumption, if wrong, makes this incorrect? Is it recorded?
[ ] What would the reviewer flag first? Fix it now.
[ ] grep for every renamed/removed symbol returns zero stale references.
[ ] Build, lint, typecheck, and the relevant tests ran — and I have the output.
```
