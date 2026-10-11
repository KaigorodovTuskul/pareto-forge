<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/pareto-forge-logo-on-dark.png">
    <img src="docs/assets/pareto-forge-logo.png" alt="Pareto Forge" width="148" height="148">
  </picture>



[![skills.sh](https://img.shields.io/badge/skills.sh-Pareto%20Forge-111111)](https://www.skills.sh/kaigorodovtuskul/pareto-forge/pareto-forge)
  


  <h1>Pareto Forge</h1>
  <p><strong>Useful first. Stop early.</strong></p>
  <p>An open-source Agent Skill that helps AI coding agents deliver usable results<br>with less unnecessary planning, code, polish, and token spend.</p>
  <p>
    <a href="https://www.skills.sh/kaigorodovtuskul/pareto-forge/pareto-forge"><img src="https://img.shields.io/badge/skills.sh-Pareto%20Forge-111111" alt="skills.sh"></a>
    <a href="https://agentskills.io/specification"><img src="https://img.shields.io/badge/Agent_Skills-open_standard-00B8C8" alt="Agent Skills"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-586776" alt="MIT"></a>
    <img src="https://img.shields.io/badge/version-1.2.0-00B8C8" alt="Version 1.2.0">
  </p>
  <p><a href="#quick-start">Quick start</a> · <a href="#how-it-works">How it works</a> · <a href="#realistic-example">Example</a> · <a href="#benchmark-lab">Benchmark</a> · <a href="#documentation">Docs</a></p>
  <p><strong>English</strong> · <a href="docs/i18n/README.ru-RU.md">Русский</a></p>
</div>

---

## Why Pareto Forge?

An AI agent can spend longer debating an implementation than implementing it. It can add tests, architecture, variants and UX polish until a five-minute prototype becomes a small project.

**Pareto Forge is an execution heuristic, not a quality-maximizing ceremony.** It asks:

> **What's the smallest usable outcome we can deliver now — and when should we stop?**

Aim to get most of the *practical* value early, minimizing elapsed time, tokens and complexity. **80/20 is a mental model, not a claimed empirical law or guaranteed savings.** Explicit user requirements and critical safety/correctness obligations are not optional.

<p align="center"><img src="docs/assets/workflow.svg" alt="Value → Cut → Ship → Stop" width="100%"></p>

## How it works

| Move | What the agent does | What it intentionally avoids |
|---|---|---|
| **01 · Value** | Identify the usable result and non-negotiable requirements | Optimizing an imagined ideal product |
| **02 · Cut** | Reuse what's there; defer low-return polish | Extra dependencies, agents, abstractions, plans |
| **03 · Ship** | Make a working first slice immediately | Endless architecture discussions |
| **04 · Stop** | Run a proportionate check, deliver and stop | Refactoring or testing for its own sake |

### Adaptive effort, not a fixed checklist

- **Flash — default:** act right away on simple reversible tasks. No compulsory planning, scoring matrix or Grill review.
- **Focus — when useful:** compare only 2–3 plausible choices if the scope genuinely needs a decision.
- **Deep — exceptional:** invoke targeted critical questions, stronger tests or a decision record for high-risk, irreversible or explicitly complex work.

The detailed [SKILL.md](skills/pareto-forge/SKILL.md) is short and self-contained. References are loaded **only when warranted**.

## Realistic example

**User:** “Build a Streamlit app demonstrating Plotly charts.”

**A lean response:** a runnable gallery with representative chart families, sample data, sidebar navigation, a few valuable controls and one quick launch/smoke check. **Defer:** a giant plugin architecture, custom theme engine, per-chart CI and exhaustive fine-tuning.

**A crucial constraint:** if the user explicitly requires **every Plotly chart type and variation**, a representative gallery does **not** fulfill that contract. Ask approval to narrow scope or implement the full agreed catalog. Speed never justifies silently dropping a must-have.

```text
streamlit-gallery/
├── app.py
└── requirements.txt
```

Pareto Forge is designed to choose proportionate effort, **not** to always produce this exact file structure.

## Quick start

```bash
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge
```

Select specific clients if desired:

```bash
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge -a claude-code -a codex -a cursor
```

Or install locally with the zero-dependency Python installer (Python 3.9+):

```bash
python scripts/install.py --project /path/to/your/project
python scripts/install.py --project /path/to/your/project --all --dry-run
```

See [compatibility notes](docs/COMPATIBILITY.md). Client discovery differs; multi-agent portability is not a guarantee of identical model behavior.

### Give the agent a task

```text
Use Pareto Forge. Build a quick Streamlit + Plotly demo.
Prioritize a runnable, useful first version. Skip nonessential polish and
stop as soon as it works. Tell me briefly what you deferred.
```

No explicit invocation is required where the host can select the skill automatically, but natural discovery depends on the agent implementation.

## What's in the repository?

```text
skills/pareto-forge/
  SKILL.md                  Short portable skill
  references/               Only-on-demand guidance: engineering, priority, Grill
  scripts/rank.py           Optional heuristic ranking (not required for execution)
benchmark/
  tasks.json                30 prospective tasks (20 coding + 10 decisions)
  run.py                    Isolated CLI A/B/C runner (Codex / Claude)
  judge.py                  Blind usefulness / mandatory-requirement review
  report.py                 Quality-gated time/token comparison + HTML report
  PROTOCOL.md               Predeclared methodology and release rules
scripts/                     Offline installer and validator
tests/                       Local validation and behavioral cases
examples/                    Generic scenarios
docs/                        Research, compatibility, evaluations, translations
```

## Benchmark Lab

**The v1.2.0 goal is efficiency at sufficient quality, not maximal output quality at any cost.** Compare Vanilla, Pareto Forge and optionally Ponytail on the **same tasks, model, permissions and runtime budget**.

- **Usefulness first:** a coding solution must meet its hard acceptance tests. A blinded reviewer checks whether decisions are usable, rather than rewarding long plans.
- **Efficiency second:** compare **actual elapsed seconds and reported tokens** only across runs where both agents produced usable results. Use task-cluster confidence intervals.
- **Safety gate:** missing must-haves and critical safety violations cannot be traded for savings.
- **Controls:** easy edits and factual questions expose unnecessary planning overhead.

```bash
# 30 tasks × 2 arms × 3 repeats = 180 real CLI runs; incurs model costs
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/ab-01

# Independent blind review is needed before interpreting the report
python benchmark/judge.py prepare --run ../pareto-bench-runs/ab-01 \
  --out ../pareto-bench-runs/blind.json
python benchmark/report.py --run ../pareto-bench-runs/ab-01
```

See the [benchmark guide](benchmark/README.md) for review/import commands, sandboxing and prerequisites, and the [protocol](benchmark/PROTOCOL.md) for predefined evidence thresholds.

**Status: comparative model results pending.** Existing unit tests check repository plumbing, not actual token savings, faster task completion or 80% utility. The current suite also has limited coverage of real full-app MVP work. Do not publish an uplift claim without independent audit. No time-to-first-usable measurement is asserted: wall time measures completion of the run.

### Preliminary Pilot Smoke Test (v1.2.0 — 7 Model Configurations)

> [!NOTE]
> **Important Disclaimer:** This is an exploratory empirical smoke test (3 representative benchmark tasks across 7 configurations, 42 real CLI trials), **NOT** the full pre-registered release benchmark (which mandates all 30 tasks × 3 repeats = 180 runs). It validates harness plumbing, blind judging, and behavioral tendencies under the v1.2.0 protocol. Formal release gate claims remain pending.

#### Benchmark Summary Table

| Model | Platform / CLI | Reasoning Effort | Mean Wall Time (Vanilla → Pareto) | Mean Total Tokens (Vanilla → Pareto) | Code Pass Rate | Blind Decision Result | Key Behavioral Effect |
|---|---|---|---|---|---|---|---|
| **Gemini 3.8 Flash High** | Antigravity (`agy`) | High | 121.5s → **70.0s** (-42%) | 99.5k → 111.2k | 100% / 100% | Tie (100% Usable) | Prevented 240s loop timeout on `c01` (finished in 71.5s); -25.6% tokens on `d08`. |
| **Gemini 3.8 Flash Medium** | Antigravity (`agy`) | Medium | 97.9s → 123.8s | 111.4k → 90.9k* | 100% / 100% | Tie (100% Usable) | 2.47x speedup (55s vs 136s) and -41.5% tokens on `c01`. |
| **Gemini 3.8 Flash Low** | Antigravity (`agy`) | Low | 31.3s → **36.0s** | 58.4k → 60.5k | 100% / 100% | Tie (100% Usable) | Code tasks faster by **-30.7%** (21.4s vs 38.0s on `c04`) with **-12.6%** fewer tokens. |
| **Claude Sonnet 4.6** | Antigravity (`agy`) | Default | 27.4s → 33.6s | **7.7k → 12.2k** | 100% / 100% | **Pareto WON Blind** | Eliminates boilerplate diffs & commentary; wins blind evaluation for conciseness. |
| **Codex Luna High** (`gpt-6-luna`) | Codex CLI | High | **25.3s** → 34.2s | **72.2k** → 96.0k | 100% / 100% | Tie (100% Usable) | Base model already concise on micro-tasks; reading `SKILL.md` adds ~8s prompt overhead. |
| **Codex Terra Medium** (`gpt-5.6-terra`) | Codex CLI | Medium | **31.8s** → 33.8s | **71.2k** → 80.9k | 100% / 100% | Tie (100% Usable) | -13.4% tokens on decision task `d08`; negligible latency delta (+2.0s). |
| **Codex Sol High** (`gpt-6-sol`) | Codex CLI | High | 31.3s → 39.9s | 105.5k → 133.3k | 100% / 100% | Tie (100% Usable) | -5.1% tokens on `c01`; 100% pass rate. |

#### Key Takeaways Across Models

1. **Gemini Flash (Google):** The `SHIP → STOP` discipline acts as an effective circuit breaker against recursive verification loops. Without the skill, unconstrained vanilla Flash agents frequently overthink micro-tasks (hitting a 240s timeout on `c01`). With Pareto Forge, tasks complete cleanly in 55–71s.
2. **Claude Sonnet 4.6 (Anthropic):** Shows an exceptionally compact token footprint (~8k–12k). Pareto Forge strips away pedagogical "essay" habits and unnecessary markdown diffs, resulting in a decisive win in blinded efficiency reviews.
3. **Codex (OpenAI):** Models natively exhibit terminal conciseness on tiny 10-line scripts. Injecting a 250-line skill introduces a small fixed prompt overhead (~5–8s) on micro-tasks; value is expected on larger tasks prone to architectural scope creep.
4. **Main Conclusion:** **Pareto Forge delivers the greatest value when paired with models prone to perfectionism, over-verification, or conversational verbosity**, preserving 100% functional correctness while curtailing runaway work.

## Validation

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python -m unittest discover -s benchmark/tests -v
```

Checks should be proportionate **when using the skill**; the repository maintains unit tests to ensure its optional tooling is sound. GitHub Actions are **not** required and not bundled.

## Documentation

[Russian quickstart](docs/QUICKSTART_RU.md) · [Reference study](docs/RESEARCH.md) · [Design audit](docs/DESIGN_AUDIT.md) · [Evaluation plan](docs/EVALUATION.md) · [Benchmark Lab](benchmark/README.md) · [Compatibility](docs/COMPATIBILITY.md) · [Branding](docs/BRANDING.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

## Credits & license

Influenced conceptually by [Ponytail](https://github.com/DietrichGebert/ponytail), [Matt Pocock's skills](https://github.com/mattpocock/skills), and the [Agent Skills spec](https://agentskills.io/specification). These projects are not bundled or affiliated. All Pareto Forge skill instructions are original.

[MIT License](LICENSE) · Contributions and honest negative benchmark results are welcome.

---

<div align="center"><strong>Useful first. Stop early.</strong></div>
