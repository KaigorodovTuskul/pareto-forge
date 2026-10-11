# How to evaluate Pareto Forge v1.2

The main question is **whether the agent delivers a sufficiently useful outcome with lower time/token cost**. A longer, more elaborate answer is not inherently better.

Real runs, CLI invocation, blind packet workflow and preregistered gates are in [`benchmark/`](../benchmark/README.md) and [`PROTOCOL.md`](../benchmark/PROTOCOL.md). No real model A/B/C results have yet been verified.

## Outcome-first rubric

**1. Usability / adequacy (primary quality floor):** can the user actually use what was delivered? Respect every explicit requirement and critical correctness/safety condition. For decisions, score `usable` separately for each anonymous answer; do not reward frameworks or elegant prose. For code, run independent functional oracles. A partial demo is *not* a completed "all features" request unless scoped with consent.

**2. Resources (primary efficiency comparison):** actual total wall clock, tokens and recorded dollars where supplied by the CLI, with missing values marked N/A. Compare only paired successes for ratios, **while also reporting all failures** to avoid survivor bias. v1.2 does not instrument time-to-first-usable; don't imply it does.

**3. Negative consequences / safeguards:** missing required behavior, unauthorized actions, nonfunctional artifacts, inaccurate test claims, or critical privacy and security omissions veto otherwise persuasive results.

**4. Stop-rule / process overhead:** does a trivial edit avoid extra planning, scoring and tests? Does a prototype stop after a credible smoke test, rather than expanding into irrelevant polish? Are riskier tasks tested proportionately?

## Design and interpretation

Use one fixed model/agent/tooling configuration per experiment. Preserve a neutral prompt without mentioning the skill in natural activation mode. Randomize order and repeat across tasks; bootstrap **tasks** rather than pretending repetitions are independent projects. Blind evaluators must not see model arms or raw metadata. Include both false positives (skill overthinks simple tasks) and false negatives (skill skips a requirement).

Do not tune the skill against a holdout and then call that holdout independent evidence. If v1.2 fails, investigate failures, produce a new version and evaluate on separate unseen tasks. Report negative/no-difference findings. Evidence of a 10–15% wall-time reduction on a limited suite must be described with the precise endpoint, CI and model configuration.

### Optional future suite: full-stack MVPs

Use realistic tasks (e.g. build a small Streamlit + Plotly gallery) with a rubric that fixes **mandatory features** in advance and marks optional polish separately. Instrument periodic artifact checkpoints inside the trial to measure **time-to-first-usable** without asking the agent to self-report it. Include a user-defined minimum usefulness threshold and explicit consent for a scoped MVP. This is **not implemented in the current 30-task corpus**.

## Unit tests are not an effectiveness benchmark

The repository's Python unit tests check parsers, report computation and packaging. They cannot demonstrate that Pareto Forge saves tokens or reduces elapsed time when deployed in real coding agents.
