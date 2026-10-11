# Reference research — Pareto Forge v1.2.0

**Reviewed:** 2026-10-11. **Scope:** public skill descriptions/READMEs and official skill-format documentation. This is a qualitative architecture study, not a benchmark of model performance or an exhaustive survey of every skill on skills.sh. Rankings, install counts and compatibility lists can change.

## Selection method

Looked for reusable mechanisms related to (1) outcome and leverage selection; (2) minimal engineering; (3) skeptical questioning / design review; (4) verification; (5) portability / skill authoring. Evaluated each reference on: *clear triggers, minimal core, reproducible examples, safety under pressure, portability, ability to test, tendency to overburden simple tasks*.

| Reference | Closest contribution | Strength | Gap / risk | Decision |
|---|---|---|---|---|
| [Ponytail](https://github.com/DietrichGebert/ponytail) ([core](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)) | Smallest complete implementation; reuse ladder | Exceptional focus on scope and avoiding bloat; portable adapters | Optimizes *how* to implement more than *what* produces value | **Adapt principle**, no copied implementation |
| [Matt Pocock: grill-me](https://www.skills.sh/mattpocock/skills/grill-me) | Decision-tree interview | Powerful challenge to weak plans | Current `grill-me` mostly delegates to `grilling`; alone it is not a self-contained method; repeated questioning can stall progress | **Self-contained, risk-gated challenge protocol** |
| [Matt Pocock: grill-with-docs](https://www.skills.sh/mattpocock/skills/grill-with-docs) | Persistent context/ADRs | Reconsidering decisions becomes harder | Heavy documentation for small tasks | **Optional decision record only** |
| [Matt Pocock: prototype](https://www.skills.sh/mattpocock/skills/prototype) | Throwaway experiment to settle a question | Strong evidence over argument | Prototype may become accidental production code | **Falsifiable experiments; remove after learning** |
| [Matt Pocock: improve-codebase-architecture](https://www.skills.sh/mattpocock/skills/improve-codebase-architecture) | Deep modules, testable interfaces | Prevents superficial abstraction proliferation | Over-architecting an MVP can itself become a detour | **Use only when architecture is the binding constraint** |
| [Matt Pocock: triage](https://www.skills.sh/mattpocock/skills/triage) | Explicit workflow states and out-of-scope knowledge | Clear handoff, disciplined scope | Issue-tracker-specific and process-heavy | **Lightweight Not now list**, no ticket machine |
| [Superpowers: brainstorming](https://www.skills.sh/obra/superpowers/brainstorming) | Validate design before expensive building | Good discovery and user alignment | Approval gates for every tiny task raise latency | **Gate deep decisions, not trivial edits** |
| [Superpowers: writing-skills](https://www.skills.sh/obra/superpowers/writing-skills) | Red/green/refactor for process skills | Test-first mindset and loophole checks | Requires model evaluation infrastructure not included here | **Provide behavioral scenarios; no fake benchmark claims** |
| [Superpowers: verification-before-completion](https://www.skills.sh/obra/superpowers/verification-before-completion) | Evidence before success claims | Directly addresses agent hallucinated completion | Verification tools not always available | **State verified/unverified explicitly** |
| [Anthropic: skill-creator](https://www.skills.sh/anthropics/skills/skill-creator) | Structured creation and eval loops | Test baseline vs skill, improve triggering | Quality improvements require actual controlled runs | **Keep eval plan, defer measured claims until runs exist** |
| [Agent Skills specification](https://agentskills.io/specification) | Common SKILL.md format and resource structure | Vendor-neutral progressive disclosure | Standard cannot force runtime adoption | **Canonical packaging standard** |
| [Vercel Labs skills CLI](https://github.com/vercel-labs/skills) | Cross-agent install paths, registry | Broad installed-client coverage | Supported list changes; installing does not prove runtime compliance | **Preferred distribution path** |

## What the survey changes

1. Make the smallest *usable outcome* explicit, and ship it before optional polish.
2. Make the grill mechanism native and independent of another installed skill.
3. Avoid enforcing process on routine tasks: Flash by default, Focus or Deep only when warranted.
4. Capture mandatory constraints *before* ROI ranking; a score cannot waive security or contracts.
5. Keep a short SKILL.md and on-demand references; this matches progressive disclosure.
6. Prefer a single portable core and official installer rather than 20 duplicated forks or unverifiable manifests.
7. Add reproducible, zero-dependency unit tests and prospective behavioral scenarios; do not state a measured performance uplift.

## Novelty / attribution boundary

Pareto, first-principles thinking, YAGNI and design reviews are general methods. Ponytail / Superpowers / Matt Pocock provide useful public examples. Pareto Forge's four-move Value/Cut/Ship/Stop workflow, criteria, example, code and documentation are independently authored as a synthesis. Nothing from those repos is bundled. See their repositories for licenses, versions and original instructions.

## Known unknowns

- Does the skill trigger reliably across target models? **Needs real-agent evaluation.**
- Does it improve user outcomes or reduce total cost? **Needs controlled baselines.**
- Does it work in all existing agent products? **No universal guarantee**; distribution via supported Agent Skills hosts, plus manual fallback.
- Do numeric prioritization scores represent measured ROI? **No**; the script is transparent shorthand and should be challenged.

## v1.2 critical refinement

Earlier versions emphasized five gates and verification quality. That framing could increase latency and token use on trivial work. The current design instead uses a Flash-first execution policy, a stop rule based on diminishing marginal value and on-demand Grill/tests. This is a design hypothesis, not an empirical improvement; the benchmark measures quality-gated resource efficiency.
