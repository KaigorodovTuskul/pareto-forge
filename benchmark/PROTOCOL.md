# Preregistered protocol — v1.2: Useful first, stop early

**Prospective. No comparative real-model results have been established.** Commit and freeze the exact skill SHA, corpus, oracles, judge rubric, CLI/model version and this protocol **before** running. Do not alter thresholds after seeing data. This protocol supersedes v1.1; never combine v1.1 and v1.2 outcomes as one experiment.

## Question and experimental unit

Does Pareto Forge produce **usable outcomes with less elapsed time / tokens**, without materially worse correctness, decision usefulness or safety? Compare identical tasks at identical model, tools, permissions and budgets, randomized order. Arms: Vanilla, Pareto Forge, and optionally a reviewed/pinned Ponytail. Each task × repeat × arm gets a fresh workspace and agent session. Forced use of the skill tests instructed application, not natural discovery; test natural mode separately.

30 cases: 20 executable small Python functions (functional/correctness controls), 10 decision/scope cases including trivial questions, fast MVP planning, explicit ALL scope, irreversible actions and access controls. **Important limitation:** small functions and written decisions do not establish efficiency on full-size Streamlit or other application builds. Later release-specific validations should add full-project tasks with externally evaluated usable checkpoints.

## What counts as a result?

- **Coding:** all independent functional tests pass, with critical static hints where applicable. Passing hidden assertions is a proxy for minimum usefulness, not full production safety. Code that fails does **not** qualify for a saving claim.
- **Decision tasks:** blind independent human or independent-model reviewers mark *each* answer `usable_A` and `usable_B`, with hard-constraint flags. Prefer minimal sufficient outcomes over polished essays; protect explicit requirements. Blind *preference* is auxiliary, not the primary benefit metric.
- **Efficiency:** actual CLI end-to-end wall time and total reported tokens. No reported tokens => `N/A`, not zero. Price is `N/A` if not reported. Do not infer time-to-first-usable from end-to-end elapsed time: that endpoint is **not instrumented** in v1.2.
- **Comparison:** calculate Pareto/opponent resource ratios only on **paired runs where both results are usable**; use log ratios and task-cluster bootstrap (repetitions are not independent task samples). Report denominators, paired selection bias and all quality outcomes.
- **Safety:** missing explicit scope, bypassed security, fabricated verification or unauthorized irreversible actions are vetoes. Extra tests or analysis are waste only when their risk-adjusted value is low, not categorically.

## Conservative experimental success gate (fixed in advance)

Automated report may label `EFFICIENCY_SUPPORTED_WITHIN_SUITE` only if:

1. All 30 cases complete across *all configured arms*, ≥3 repetitions each, non-mock real adapter, no failed CLI runs, all decision pairs judged.
2. Pareto has **no recorded hard requirement violations** and no blind safety vetoes.
3. Against every comparator, task-cluster bootstrap **95% lower confidence limits** on the paired difference in coding success rates **and** blinded decision usability rates are at least **−5 percentage points** (predefined non-inferiority tolerance; does not justify silently skipping explicit user requirements).
4. Against every comparator, the **upper 95% confidence bound** of Pareto/opponent elapsed-time **or** token ratio, among paired usable results, is below **0.90** (at least 10% resource reduction within this suite). For any *other measured* resource among time/tokens, the upper CI must not exceed **1.10** (no demonstrated material regression). Missing telemetry cannot satisfy that metric.
5. An **independent manual auditor** checks raw transcripts, task-mismatch and grader blind spots, selection bias, judge labels, unusual failures and versions. A generated label is NOT sufficient for publication.

`NOT_DEMONSTRATED` means a completed but unconvincing result. `INSUFFICIENT_EVIDENCE` means the required data or complete review is absent. `SMOKE_TEST_ONLY` never proves efficacy. Do not cherry-pick tasks or rerun until confidence intervals look attractive. Negative findings should be public too.

## Interpretation

The 5 pp quality margin and 10% savings threshold are **product decision criteria**, not universal scientific standards. A +13% effect can be worthwhile even if it fails this particular strong-evidence gate; disclose estimates and uncertainty. Test controls for regressions (trivial tasks are especially important). Ratios conditional on both arms succeeding can overstate practical value; **always** report raw success, end-to-end resource use by arm, and unsuccessful runs alongside eligible ratios.

**The 80/20 heuristic is not an observable percentage of value in this benchmark**. No claim of "80% result at 20% effort" is warranted unless a separate study operationalizes and measures actual end-user utility and effort.

## Reproducibility & privacy

Only use an ephemeral isolated OS/container or VM with secrets and network restricted. Running model-generated Python is unsafe without sandboxing; agent workspace permissions alone do not sandbox the grader. Review any data before publishing JSONL traces. Freeze hashes and CLI versions, redact secrets, publish code and protocol without changing data after the fact.
