# Pareto Forge — Efficiency Benchmark Lab v1.2

**Primary research question:** Does Pareto Forge deliver sufficiently usable outcomes in **less time and fewer tokens**, rather than merely producing better-looking plans?

There are **no real model A/B/C measurements** bundled. Mock tests validate the harness and can never be published as savings evidence.

## Existing 30-case suite

- **20 Python code tasks:** deterministic independent hidden I/O oracles; functional pass requires 100% of required assertions.
- **10 decision/control tasks:** blinded independent reviewer judges individual answer usefulness and critical constraints, then comparative preference. These now include an explicitly scoped Streamlit/Plotly MVP and an ambiguous **ALL chart variations** request.
- Outputs: full stdout/stderr and JSONL traces, time, usage when provided by CLI, functional scores, blind usefulness labels, `summary.json`, `metrics.csv` and offline HTML charts.

**Limits:** These are small functions and written plans, not actual full-app development. No measured time-to-first-usable. The project explicitly preserves full mandatory requirements: a user-requested "all" cannot be silently downgraded to a small MVP.

## Setup

Requires Python 3.9+, an authenticated Codex or Claude CLI, a pinned model ID, and a disposable external sandbox/container/VM with no sensitive host files, secrets or production access. Executing generated code is risky; CLI workspace restrictions and `python -I` do not replace OS isolation. **You must supply the isolated environment**; the harness does not build one.

For Ponytail comparator, review a pinned upstream skill and provide its local path. It is not bundled or downloaded.

## Real A/B (180 runs at 3 repeats)

```bash
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/ab-v12
```

For Claude Code:

```bash
python benchmark/run.py --adapter claude --model YOUR_PINNED_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/claude-v12
```

For A/B/C (270 runs):

```bash
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --ponytail-skill /path/to/pinned/ponytail/skills/ponytail \
  --repeats 3 --out ../pareto-bench-runs/abc-v12
```

Runs are randomized, each using a fresh workspace. Default `--activation forced` explicitly instructs agent to read skill, while `--activation natural` separately tests passive discovery; **do not pool**. Real CLI runs can incur charges. Never mistake `--adapter mock` for evaluation.

## Blind independent decision review

Create the packet outside the raw run directory and provide only that packet to reviewer:

```bash
python benchmark/judge.py prepare \
  --run ../pareto-bench-runs/ab-v12 \
  --out ../pareto-bench-runs/ab-blind.json
```

`private_blind_mapping.json` stays in the run folder. Never show it to the reviewer.

Judge schema (example, **not a real measurement**):

```json
{
  "judge": "independent-human",
  "judgments": [{
    "id": "OPAQUE_ID_FROM_PACKET", "winner": "tie",
    "usable_A": true, "usable_B": true,
    "hard_violation_A": false, "hard_violation_B": false,
    "reason": "Both are usable; neither contains critical omissions."
  }]
}
```

Or optional independent OpenRouter model (review and pin model, handle credentials locally):

```bash
python benchmark/judge.py score-openrouter \
  --blind ../pareto-bench-runs/ab-blind.json \
  --out ../pareto-bench-runs/ab-judgments.json \
  --model YOUR_INDEPENDENT_JUDGE_MODEL
```

Import after full review:

```bash
python benchmark/judge.py import \
  --run ../pareto-bench-runs/ab-v12 \
  --judgments ../pareto-bench-runs/ab-judgments.json
python benchmark/report.py --run ../pareto-bench-runs/ab-v12
```

The report uses task-cluster bootstrap confidence intervals for **quality non-inferiority** and paired usable-run time/token efficiency. Costs/tokens are `N/A` when telemetry is incomplete. The numeric verdict is **not approval to advertise** without human trace review. Read [PROTOCOL.md](PROTOCOL.md) before running: all thresholds must be frozen up front.

## Smoke test (not a model experiment)

```bash
python benchmark/run.py --adapter mock --repeats 1 \
  --case c01-normalize --case d08-simple --out ../pareto-bench-smoke
python benchmark/report.py --run ../pareto-bench-smoke
```

Expected verdict: `SMOKE_TEST_ONLY`, regardless of any transport artifacts. No automatic CI required.
