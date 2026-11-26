# Agent Standard (AG)

The house bar for AI agents Maestro builds as PRODUCTS (prompts, tools, loops, memory, evals) — primary
in maestro-adlc and maestro-enterprise, applicable anywhere a feature calls an LLM. It does not govern
Maestro's own workflow agents (those follow the engine rules). Levels and precedence:
[README.md](README.md).

## A. Mission and shape

```text
AG-01 MUST   One-sentence mission, explicit non-goals, and the user it serves. Behavior outside the
             mission is refused or handed off, and that is tested.
AG-02 SHOULD Simplest architecture that passes the evals: a single call, then a fixed workflow (chain,
             route, parallelize), then an agent loop, then multiple agents — escalate a level only when
             eval results show the simpler level fails.
AG-03 SHOULD Least tools. Each tool has one clear job, a description that says when to use and when NOT
             to, typed parameters, and error messages the model can act on.
```

## B. Evals are the gate

```text
AG-04 MUST   A behavior eval suite exists before the agent is called done: happy path, edge cases,
             refusals and out-of-scope, adversarial and injection cases, and regressions for every fixed
             bug. Suites run on every prompt, tool, or model change.
AG-05 MUST   Pass criteria are defined before running (thresholds per suite), and results are recorded
             with model version, prompt version, and cost. No "it looked good in a few tries".
AG-06 SHOULD Graders are deterministic where possible (exact checks, schemas, assertions); LLM-as-judge
             graders use a rubric, are spot-checked against human labels, and never grade their own output.
```

## C. Safety and control (floor)

```text
AG-07 MUST (floor) Untrusted content — user input, retrieved documents, web pages, tool and API output —
             is data, never instructions. The agent's authority comes only from its system prompt and
             its human principal. Injection cases live in the eval suite.
AG-08 MUST (floor) Irreversible or outward actions (payments, sending messages, deleting data, publishing)
             require explicit human confirmation or a pre-approved policy, and are logged.
AG-09 MUST   Loops are bounded: max steps, max tokens/cost, wall-clock timeout. On hitting a bound the
             agent stops with a useful status, not silence.
AG-10 MUST   Honest uncertainty: the agent says when it does not know, never fabricates citations, tool
             results, or facts, and this is evaluated.
```

## D. Operate it like software

```text
AG-11 SHOULD Every run is traced: inputs, tool calls, outputs, latency, tokens, cost — with PII redacted.
AG-12 SHOULD Prompts are versioned files with a changelog; no secrets in prompts; model versions pinned and
             the eval suite re-run on any model upgrade.
AG-13 SHOULD High-stakes outputs get an independent verification pass that does not see the producer's
             reasoning — only the task, the output, and the rubric (blind verification).
AG-14 SHOULD Model choice is made by eval results and cost per successful task, not by default.
```

## Agent review checklist

```text
[ ] Mission, non-goals, and user stated (AG-01); architecture level justified by evals (AG-02)
[ ] Tool set minimal with when/when-not descriptions (AG-03)
[ ] Eval suite covers happy / edge / refusal / injection / regression with thresholds (AG-04/05)
[ ] Untrusted content handled as data; outward actions confirmed (AG-07/08)
[ ] Loop bounds and stop status defined (AG-09); uncertainty behavior evaluated (AG-10)
```
