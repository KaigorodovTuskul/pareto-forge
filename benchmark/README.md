# Pareto Forge Benchmark Lab

**A real experimental harness, not a dashboard of invented improvements.** Run the same 30 prospective tasks with a baseline agent, Pareto Forge, and optionally a locally pinned Ponytail skill. Save original CLI traces; grade code by hidden, deterministic functional tests; grade decisions by blind paired reviews; compare outcome quality, time, tokens and cost when actually reported.

**No model benchmark has been executed in this repository.** `benchmark/` contains the tools to run one, not results. Mock-adapter smoke tests are explicitly ineligible for efficacy conclusions.

## Corpus and scoring

- [`tasks.json`](tasks.json): **30 tasks** = 20 independent executable Python stdlib coding prompts + 10 judgment/control prompts. Every task gets an independent fresh workspace.
- [`graders/code_oracles.py`](graders/code_oracles.py): private-to-agent deterministic I/O tests; not copied into agent workspaces. All tests must pass for a coding task to count as solved. A static flag is added for the timing-safe HMAC task; do not infer formal constant-time guarantees from a code scan.
- [`judge.py`](judge.py): blinded A/B comparisons on qualitative decisions. Optional OpenRouter evaluation, or supply independent human grades using the same JSON schema. Never use the target agent or the same session as its own judge.
- [`report.py`](report.py): independent summary and charts in a **self-contained HTML report**, plus `metrics.csv` and `summary.json`. Report flags inconclusive/missing data and has preregistered conservative criteria in [`PROTOCOL.md`](PROTOCOL.md).

## Prerequisites

- Python **3.9+**, no required pip dependencies for the harness.
- An authenticated **Codex CLI** (`codex`) or **Claude Code** (`claude`) on PATH, and a **pinned model ID**.
- If comparing Ponytail, manually download/review and pin a version: supply the **local** directory containing its `SKILL.md`; it is **not bundled** and not fetched automatically.
- A disposable **sandbox/container/VM with network and secrets restricted**, especially when executing agent-produced code. Workspace-write in an agent is *not* a complete OS-level security boundary for malicious grader execution. **Never run agent-generated Python with your production credentials.**

## Run A/B (30 tasks × 2 arms × 3 repeats = 180 real trials)

From repository root:

```bash
# choose an already-authenticated CLI and an exact model for reproducibility
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/ab-01

# Alternative adapter (same benchmark, different experiment)
python benchmark/run.py --adapter claude --model YOUR_PINNED_CLAUDE_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/claude-ab-01
```

For **A/B/C** (30 tasks × 3 arms × 3 repeats = **270** trials):

```bash
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --ponytail-skill /absolute/path/to/ponytail/skills/ponytail \
  --repeats 3 --out ../pareto-bench-runs/abc-01
```

The runner randomizes the **order** of all runs using a recorded seed, creates a new workspace and agent session per trial, records the exact `SKILL.md` hash, saves stdout/stderr, an event `trace.jsonl`, `grading.json`, `timing.json`, and appends to `events.jsonl`. No automatic rerun of failed API calls (because that can make sample counts misleading). The runner refuses a nonempty output destination; runs are immutable.

The default `--activation forced` explicitly asks treatment agents to read their installed skill. **This tests prompt-assisted use, not passive skill discovery.** To investigate natural discovery separately, run another experiment using `--activation natural`. Do not combine arms or settings across experimental designs.

## Blind review

Prepare packet **outside** raw run directory and give only that packet to an independent reviewer:

```bash
python benchmark/judge.py prepare \
  --run ../pareto-bench-runs/abc-01 \
  --out ../pareto-bench-runs/blind-packet.json
```

`abc-01/private_blind_mapping.json` contains arm identities. **Never provide it to the reviewer.** The packet has candidate answers anonymized as A/B, with randomized order and a neutral scoring rubric. To use an independent model via OpenRouter:

```bash
# Set your key securely in environment (never commit credentials).
export OPENROUTER_API_KEY='...'
python benchmark/judge.py score-openrouter \
  --blind ../pareto-bench-runs/blind-packet.json \
  --out ../pareto-bench-runs/judgments.json \
  --model YOUR_INDEPENDENT_JUDGE_MODEL

python benchmark/judge.py import \
  --run ../pareto-bench-runs/abc-01 \
  --judgments ../pareto-bench-runs/judgments.json
```

For **human judgment**, populate `judgments.json` as

```json
{
  "judge": "independent-human",
  "judgments": [
    {
      "id": "OPAQUE_PAIR_ID_FROM_BLIND_PACKET",
      "winner": "A",
      "hard_violation_A": false,
      "hard_violation_B": false,
      "reason": "A meets the stated audit constraint and gives a credible validation plan."
    }
  ]
}
```

These values are **format examples**, not measured outcomes. Score every pair and review at least a subset manually before treating model judgments as evidence. Do **not** let Antigravity infer arm identity from repository history or private mapping while judging.

## Report

```bash
python benchmark/report.py --run ../pareto-bench-runs/abc-01
# open ../pareto-bench-runs/abc-01/report.html
```

A run produces `summary.json`, `metrics.csv`, and `report.html`. All figures reflect present evidence only; costs and tokens remain N/A when the CLI does not report them. Comparison uses *paired observations by task/repetition*, with a task-cluster bootstrap confidence interval for code pass-rate difference, and task-cluster bootstrapping plus a descriptive Wilson lower bound for blinded preference proportions.

### Quick offline smoke test (not an efficacy experiment)

```bash
python benchmark/run.py --adapter mock --repeats 1 \
  --case c01-normalize --case d01-onboarding \
  --out ../pareto-bench-runs/smoke-01
python benchmark/report.py --run ../pareto-bench-runs/smoke-01
```

The report **must** read `SMOKE_TEST_ONLY`. Use `python -m unittest discover -s benchmark/tests -v` for harness tests. Never include mock numbers in `README.md` benchmarks.

## Methodological limits

- Tiny coding tasks are only a synthetic *transfer proxy*, not proof about large codebases. Preregister and later add harder, realistic repo tasks before making broad claims.
- The Ponytail arm is optional; **do not call A/B results A/B/C** if no reviewed local Ponytail skill was supplied.
- Install both variants using their same portable markdown skill format, keeping externally configured rules as controlled as possible. Record CLI version, model ID, context and environment, and any observed differences.
- Judge bias, contamination from existing global skills, differing system prompts, randomness, tool access and network variance can distort results. Repeat with independent seeds/models and spot-check decisions.
- No measured cost/latency claims without telemetry; no reduction percentages if tasks or outcomes are not comparable. **Never conflate fewer tokens with a better result.**
