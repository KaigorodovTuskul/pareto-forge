# Pareto Forge v1.2 — adversarial design audit

**Scope:** reasoned static audit of the rewritten skill and prospective efficiency benchmark; not an external independent model audit and not proof of behavioral improvement.

| Challenge | Finding | Decision / mitigation | Evidence still required |
|---|---|---|---|
| Did v1.1 optimize quality instead of efficiency? | Yes: five obligatory gates and Focus as default can spend too much time planning and verifying. | Default to **Flash**; four *internal* moves; Grill/scoring/record only by exception. | Real wall-time and token A/B |
| Does "80% value at 20% effort" describe measurable success? | It is a heuristic, with no universal 80% utility scale. | Benchmark **functional adequacy and resources**, not fictional utility percentages. | User study for subjective value |
| Could simplification quietly violate "all" or an explicit contract? | Yes. An MVP cannot substitute for explicit exhaustive scope. | Ask approval to narrow, otherwise honor agreed complete acceptance criteria. | Traces on scope-ambiguity tasks |
| Does minimal checking cause unsafe code? | In some tasks, yes: authentication, payments, irreversible changes and production workflows need safeguards. | Cheap proportionate checks for demos; strong tests as **must-have** where risk justifies them. | Security and safety blind audits |
| Is it still too wordy? | Even a short skill can trigger process theater if it always prints steps. | Internal guidance; only brief after-action report, not mandatory headers. | Real trace/token analysis |
| Can shorter answers fool judges? | Yes, if judged on brevity or buzzwords. | Mark **usable for each arm**, blind output identities; don't use length as savings proxy. | Independent blinded review |
| Do efficiency ratios bias toward survivors? | Yes, condition on both arms succeeding. | Report raw failure rates, usable-pair denominators and selection-bias warnings; quality CI gate. | Sensitivity analysis by task |
| Are 30 microcases enough to prove real app savings? | No. They test tiny coding changes and decisions, not large working applications. | Disclose this limitation; separately design full-stack benchmark with checkpoints. | Holdout realistic app cases |
| Are token figures always available? | No; CLIs differ, and cache/pricing affect costs. | N/A for missing telemetry; report end-to-end wall time separately. | Check parser against actual CLI versions |
| Could the grader be unsafe to run locally? | Generated code is arbitrary code; `python -I` only isolates imports. | Run benchmark only in an ephemeral OS sandbox/container with no secrets. | Independent environment review |
| Is a sophisticated optimization engine necessary? | No evidence. It would violate the product's own goal. | No runtime framework, no remote agent dependencies, optional ranking utility only. | Real user feedback |

## Release readiness

- Canonical v1.2 `SKILL.md` with Agent Skills frontmatter and on-demand reference files.
- `AGENTS.md` fallback and bilingual GitHub README describe the **same** Flash-first philosophy.
- Existing local tests and updated benchmark tests check packaging, grader behavior and report integrity.
- No GitHub Actions workflow needed; the repository can run checks manually.
- **No independent A/B/C results yet.** No claim of proven speedup, token saving, or universal 80/20 outcomes.

## Next experiments

Run A/B/C on a frozen corpus and exact pinned model IDs; review abnormal failures and judge disagreements. Afterward test on unseen, more realistic app-generation tasks with consent-defined minimum scope and observable time-to-first-usable checkpoints. If extra rules increase cost without measurable usefulness, remove them rather than polishing the prose.
