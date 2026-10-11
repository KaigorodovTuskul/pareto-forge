# Preregistered benchmark protocol

Status: **prospective — no efficacy run has been completed**. Freeze this document, `tasks.json`, code oracles and model/config hashes **before running**; commit the frozen set in git.

## Experimental unit and comparators

Each task × repetition × arm receives a fresh independent workspace and agent session. Use pinned agent version, model, tool permissions and environment. Randomize order with a recorded seed. Baseline: vanilla. Treatment: Pareto Forge. Comparator if available: exact reviewed/pinned Ponytail version. Forced invocation is a separate estimand from natural activation.

Primary code endpoint: *all independently checked requirements pass* per coding task (`1` or `0`), with 20 tasks. Partial assertion pass fractions are descriptive only. Primary judgment endpoint: blinded head-to-head preference on 10 decision tasks, including the two simple/control tasks. Reviewer sees prompts and anonymous outputs, but no source or arm identities. Explicit hard-constraint failure vetoes quality.

Secondary endpoints: observed wall-clock duration, output/code complexity, consumed tokens, measured USD cost, subjective calibration and cross-case consistency. No telemetry => N/A. Quantities such as lines changed, tool actions and dependencies may be reported descriptively but **never** as the sole quality endpoint. Agent harness exit failures invalidate published claims pending root-cause audit.

## Conservative release claim gate

The automated report outputs `SUPPORTED_WITHIN_SUITE` **only if**:

1. The full 30-task suite ran in both (and when present all three) arms with at least 3 repetitions per task, *real* CLI adapters, and no command failures or missing blind judgments.
2. For coding tasks, Pareto's mean binary success advantage over each comparator is **positive with a 95% task-cluster bootstrap CI whose lower bound exceeds zero**.
3. On blinded decision comparisons, Pareto wins more than half with a **Wilson 95% lower bound > 0.5 **and task-cluster bootstrap 95% lower bound > 0.5**** against each available comparator; ties are not counted as wins.
4. No recorded hard-constraint violations for Pareto, including during trivial/control tasks.
5. An independent reviewer spot-checks scored judgments, full traces, execution environment and potential grader blind spots. (This **manual audit is not detectable by code**; the automated label is not release approval.)

Report `INSUFFICIENT_EVIDENCE` for incomplete runs; `NOT_DEMONSTRATED` for a complete but unconvincing test. `SMOKE_TEST_ONLY` for transport mocks. A completed test failing to show benefit is a *negative or inconclusive result* to document; do not rerun until a p-value becomes favorable or selectively omit failed cases.

## Statistical interpretation

The cluster bootstrap samples **tasks**, preserving within-task repetitions, so repeated trials are not incorrectly presented as 180 independent different tasks. The Wilson interval estimates a proportion on blind comparisons; because repeats share prompts it is optimistic on its own, so the release gate also requires a **task-cluster bootstrap CI** for the blind win rate. The predefined 30 tasks may not represent external distributions; even a positive result supports only **this suite/model/toolchain**, not the blanket statement "Pareto Forge improves AI agents by X%".

No benchmark results should be inserted into the public README unless the evidence gate and independent review are satisfied. If evidence passes, README must name model/agent versions, tasks, repetitions, date, comparisons, outcomes/CI, raw reports and non-generalizability note. Do not conceal unfavorable endpoints (cost, latency, controls) or unknown readings.

## Reproducibility and publication privacy

Never publish secrets, full private user workspaces, internal account data, external cookies, real production code, or raw traces that contain sensitive information. `report.html` and summary JSON may be published after manual redaction/audit; checksums and tool versions are required. Do not add a GitHub badge claiming "SOTA" or "proven 80/20". Preserve historical raw results privately; any selected publication must disclose the selection rule.
