<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/pareto-forge-logo-on-dark.png">
    <img src="docs/assets/pareto-forge-logo.png" alt="Pareto Forge — converging paths meet at one high-leverage point" width="160" height="160">
  </picture>



[![skills.sh](https://img.shields.io/badge/skills.sh-Pareto%20Forge-111111)](https://www.skills.sh/kaigorodovtuskul/pareto-forge/pareto-forge)
  


  <h1>Pareto Forge</h1>

  <p><strong>Do less. Ship what matters.</strong></p>
  <p>An outcome-first skill that helps AI agents prioritize high-leverage work,<br>challenge assumptions, and deliver the smallest complete solution.</p>

  <p>
    <a href="https://agentskills.io/specification"><img src="https://img.shields.io/badge/Agent_Skills-open_standard-00B8C8?style=flat-square" alt="Agent Skills open standard"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-586776?style=flat-square" alt="MIT license"></a>
    <a href="docs/COMPATIBILITY.md"><img src="https://img.shields.io/badge/agents-cross--platform-586776?style=flat-square" alt="Cross-platform agent support"></a>
    <img src="https://img.shields.io/badge/runtime_deps-zero-2B8C67?style=flat-square" alt="Zero required runtime dependencies">
  </p>

  <p>
    <a href="#quick-start"><strong>Quick start</strong></a> ·
    <a href="#why-pareto-forge">Why Pareto Forge?</a> ·
    <a href="#how-it-works">How it works</a> ·
    <a href="#examples">Examples</a> ·
    <a href="#benchmark-lab">Benchmark Lab</a> ·
    <a href="#documentation">Docs</a>
  </p>

  <p><strong>English</strong> · <a href="docs/i18n/README.ru-RU.md">Русский</a></p>
</div>

---

## What is Pareto Forge?

**Pareto Forge is a portable [Agent Skill](https://agentskills.io/specification) for better decisions before faster execution.** It combines Pareto-style prioritization, adversarial questioning inspired by *Grill Me*, and minimal-complete engineering inspired by *Ponytail*.

Instead of immediately planning or building everything a request mentions, the agent first asks:

> **What is the smallest set of actions that can deliver the outcome — without dropping essential requirements?**

It then identifies what to **defer**, tries to disprove its preferred approach, executes the simplest credible path, and verifies the result. It is **not** a new LLM, an MCP server, or a promise that every problem follows an exact 80/20 distribution.

<p align="center"><img src="docs/assets/workflow.svg" alt="The five Pareto Forge gates: Outcome, Leverage, Challenge, Minimize, Verify" width="100%"></p>

## Why Pareto Forge?

### The problem with implementation-first agents

AI coding agents can create a lot of output. That is not always the same as creating value.

- **Scope inflation** — implementing every requested idea rather than separating the must-haves from the nice-to-haves.
- **Premature complexity** — adding orchestration, services, frameworks, or dependencies before they are needed.
- **Unchallenged assumptions** — confidently choosing an architecture before validating the biggest uncertainty.
- **Unverified completion** — treating produced code or a polished plan as proof that the user's outcome was achieved.

Pareto Forge changes the *order of decisions*, not the underlying model:

| Without an outcome-first workflow | With Pareto Forge |
|---|---|
| Build the full feature list | Identify the smallest sufficient scope |
| Optimize for visible activity | Optimize for a defined outcome |
| Add abstractions for hypothetical needs | Reuse → simplify → write only what is necessary |
| Accept the first plausible plan | Attack its most consequential assumptions |
| Announce completion | Check the result against evidence |

### Core design: agent judgment × deterministic guardrails

**Agent judgment handles ambiguity:** determine the outcome, evaluate options, ask high-leverage questions, and explain tradeoffs.

**Deterministic utilities handle checkable mechanics:** an optional local ranking script validates candidate scores, mandatory requirements, dependencies, and effort budgets. Repository tests verify the skill's structure and tools; the independent benchmark harness is separate.

These utilities **do not guarantee** that the agent selects the best option, that estimates are objectively correct, or that the skill activates identically in every host.

## How it works

| Gate | Question | Expected result |
|---|---|---|
| **01 · Outcome** | What measurable result matters, and what must not be compromised? | Success criteria + hard constraints |
| **02 · Leverage** | Which few actions offer the strongest evidence-backed impact? | Shortlist + explicit **Not now** |
| **03 · Challenge** | What assumption could make our preferred path fail? | Counterexample + cheapest useful test |
| **04 · Minimize** | Can we avoid, remove, reuse, or simplify before building? | Smallest complete implementation |
| **05 · Verify** | Did the result satisfy the success criteria? | Evidence, remaining risks, stop condition |

### Adaptive depth — no process theater

| Mode | Use when | What the agent does |
|---|---|---|
| **Flash** | Small, reversible tasks | Choose → simplify → check |
| **Focus** *(default)* | Features and everyday decisions | Compare options, challenge assumptions, defer low-value work |
| **Deep** | Expensive, architectural, or hard-to-reverse decisions | Detailed grill, experiment plan, decision record, rollback |

The agent should choose the **lightest safe mode**. You can request a mode explicitly.

## Quick start

### 1. Install with the Skills CLI

Install Pareto Forge directly from its public GitHub repository:

```bash
# Install interactively using the open-source Skills CLI
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge

# Install for specific clients
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge -a claude-code -a cursor -a codex

# Install for clients recognized by your Skills CLI version
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge --agent '*'
```

The installer is maintained by [Vercel Labs](https://github.com/vercel-labs/skills) and is not bundled in this repository. Review third-party installer permissions before running it.

### 2. Or install offline — no Node.js required

Python 3.9+ is required **only for the optional local tools and installer**, not to read the skill itself.

```bash
# Run from the downloaded Pareto Forge repository
python scripts/install.py --project /path/to/your/project

# Preview all local installer's known agent targets without writing
python scripts/install.py --project /path/to/your/project --all --dry-run

# Explicit target(s)
python scripts/install.py --project /path/to/your/project -a claude-code -a opencode
```

Windows PowerShell:

```powershell
py scripts/install.py --project "C:\path\to\your\project" -a claude-code
```

Existing skill directories are **not overwritten** unless you pass `--force`. For manual installation and host-specific paths, see [Compatibility & Installation](docs/COMPATIBILITY.md).

### 3. Give your agent an outcome

Paste into a skill-capable agent:

```text
Use Pareto Forge in focus mode.
I need to ship a usable version of [feature] this week.
Define the outcome, identify the highest-leverage scope,
challenge the biggest assumption, and tell me what to defer.
Then implement and verify the smallest complete solution.
```

Or for a demanding architecture review:

```text
Pareto Forge, deep mode: grill this architecture.
Ask only questions that could materially change the decision.
Show the cheaper alternatives and a falsifiable experiment.
```

Some hosts expose skills as slash commands, but **natural-language invocation is the portable path**; slash-command behavior depends on the client.

## Supported agents

Pareto Forge is vendor-neutral Markdown with a standard `SKILL.md` entry point. It is designed for clients that support the [Agent Skills format](https://agentskills.io/specification).

| Agent | Installation path |
|---|---|
| **Claude Code** | Skills CLI or `.claude/skills/` |
| **OpenAI Codex** | Skills CLI or `.agents/skills/` |
| **Cursor** | Skills CLI or `.agents/skills/` |
| **Gemini CLI** | Skills CLI or a supported skills folder |
| **OpenCode** | Skills CLI or `.opencode/skills/` |
| **GitHub Copilot, Cline, Windsurf and others** | Skills CLI / host-specific instructions |

**Compatibility means portable format and documented installation options, not guaranteed behavior in every model or agent.** The exact host list evolves; check the [compatibility matrix](docs/COMPATIBILITY.md) and [Skills CLI registry](https://github.com/vercel-labs/skills#supported-agents).

## Examples

### Example 1 · A lean onboarding release

**Request:** “We have 15 feature ideas and one week to launch an onboarding flow. Where should we start?”

<details open>
<summary><strong>What the Pareto Forge workflow would produce</strong></summary>

- **Outcome:** teammates complete onboarding reliably, with accessibility and correct permissions.
- **Hard requirements:** access controls, auditing, existing integration contracts, localization.
- **High-leverage pilot:** reuse the existing invitation API and validate three critical user journeys.
- **Not now:** a new workflow engine, speculative integrations and dashboard decoration.
- **Grill question:** does the small pilot handle expired invitations and cross-team roles?
- **Verify:** run integration and accessibility tests, capture actual completion rate, expand only if warranted.

This is an **illustrative decision process**, not a measured 80/20 gain. [Full walkthrough →](examples/release-planning.md)

</details>

### Example 2 · A deceptively simple UI feature

**Request:** “Add a calendar picker.”

The agent checks existing components and the native platform first. If a native date input satisfies accessibility, browser support, localization, and product requirements, it avoids an unnecessary dependency. If the product needs a richer picker, **simplicity does not override correctness**. [Web app example →](examples/web-app.md)

## Optional deterministic prioritizer

A built-in zero-dependency Python tool can rank **comparable** options while respecting mandatory work and explicit dependencies:

```bash
python skills/pareto-forge/scripts/rank.py \
  --input examples/candidates.json \
  --budget 6
```

**Scoring heuristic:** `impact × confidence ÷ effort`. The values are user/model estimates, **not measured ROI**, and the selection is greedy rather than a mathematically optimal portfolio. Important decisions still require judgment and evidence.

### What's inside

```text
pareto-forge/
├── README.md                    Project overview and usage
├── skills/pareto-forge/
│   ├── SKILL.md                 Canonical portable skill
│   ├── references/              Prioritization, grill, engineering, outputs
│   ├── assets/                  Decision-record template
│   └── scripts/rank.py          Optional local priority helper
├── scripts/                     Offline installer and validator
├── tests/                       Automated checks and behavioral eval cases
├── benchmark/                   30-task A/B/C CLI, independent grading, HTML reports
├── examples/                    Release-planning and web-app walkthroughs
└── docs/                        Research, audit, compatibility, guides
    ├── assets/                  Logo and workflow diagram
    └── i18n/                    Localized documentation
```

## Benchmark Lab

**30 prospective scenarios, zero published performance claims.** The repository now includes a reproducible A/B/C evaluation harness:

- **20 executable Python tasks:** independent hidden functional graders; an answer must pass every assertion to count as solved.
- **10 decision/control tasks:** independent, blinded pairwise evaluation with explicit hard-constraint vetoes.
- **Arms:** vanilla vs Pareto Forge, optionally a pinned and reviewed local Ponytail skill.
- **Evidence:** real CLI runs through Codex or Claude, per-run `trace.jsonl`, timing and token/cost telemetry when available, task-cluster confidence intervals, and a self-contained HTML report with charts.

```bash
# Three repeats × 30 tasks × two arms = 180 real trials.
python benchmark/run.py --adapter codex --model YOUR_PINNED_MODEL_ID \
  --repeats 3 --out ../pareto-bench-runs/ab-01

python benchmark/judge.py prepare \
  --run ../pareto-bench-runs/ab-01 \
  --out ../pareto-bench-runs/blind-ab.json

# See benchmark/README.md for independent judgment + optional Ponytail comparator.
python benchmark/report.py --run ../pareto-bench-runs/ab-01
```

**Current status: unbenchmarked.** No model A/B/C experiment has been executed or verified. Mock adapter tests validate the harness only and must never be cited as results. Real trials may incur API charges and execute agent-created code; **run only inside a disposable sandbox**. See the [Benchmark Lab guide](benchmark/README.md) and [preregistered protocol](benchmark/PROTOCOL.md). Only independent, audited evidence is eligible for publication in this README.

## Validation & limitations

This repository includes structural validation, Python unit tests, installation tests, prospective behavioral cases, and an independent 30-task benchmark harness (not yet executed against an LLM). Run the local checks with:

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python -m unittest discover -s benchmark/tests -v
```

**What we have not established:** independent performance benchmarks, measured token savings, guaranteed 80/20 gains, or end-to-end behavioral parity across every AI host. See the [evaluation plan](docs/EVALUATION.md) before making claims about effectiveness.

The five gates are instructions for the agent, **not an external enforcement engine**. Mandatory legal, security, safety, and user requirements always take precedence over optimization.

## Documentation

| Document | What you'll find |
|---|---|
| [Quickstart — Russian](docs/QUICKSTART_RU.md) | Short Russian-language installation guide |
| [Research](docs/RESEARCH.md) | Reference skills and design decisions |
| [Design audit](docs/DESIGN_AUDIT.md) | Assumptions, critiques, and mitigations |
| [Compatibility](docs/COMPATIBILITY.md) | Agent-specific discovery paths and caveats |
| [Evaluation](docs/EVALUATION.md) | How to measure real behavior and quality |
| [Benchmark Lab](benchmark/README.md) | Real agent A/B/C runner, graders, raw traces and HTML report |
| [Branding](docs/BRANDING.md) | Logo assets and usage |
| [Contributing](CONTRIBUTING.md) | Propose improvements and tests |
| [Security](SECURITY.md) | Trust model and responsible reporting |

## Acknowledgments

Pareto Forge draws conceptual inspiration from [Ponytail](https://github.com/DietrichGebert/ponytail), [Matt Pocock's skills](https://github.com/mattpocock/skills), [Superpowers](https://github.com/obra/superpowers), and the open [Agent Skills specification](https://agentskills.io/specification). The skill instructions are original; the referenced projects are **not bundled or affiliated**.

## Contributing & license

Contributions are welcome, especially reproducible failure cases and before/after evaluations. See [CONTRIBUTING.md](CONTRIBUTING.md).

Distributed under the [MIT License](LICENSE). Please review [SECURITY.md](SECURITY.md) before integrating any third-party agent skill into a sensitive development environment.

---

<div align="center">
  <sub><strong>Optimize for outcomes, not output.</strong> · Pareto Forge</sub>
</div>
