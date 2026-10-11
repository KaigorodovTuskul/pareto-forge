# Design audit — adversarial review

**Method:** a self-contained review modeled on the *questions* approach used by grilling skills. This is a documented reasoning/design audit, **not** a claim that an external autonomous agent ran or that a named third-party skill approved this project.

## Challenge log

| Challenge | Finding | Decision / mitigation | Status |
|---|---|---|---|
| Is this just Ponytail with a new name? | Ponytail targets minimal implementation; the missing step is choosing high-leverage *outcomes*. | Add an explicit LEVERAGE gate before implementation; independent text and scripts. | Addressed by design |
| Can agents misuse “80/20” as license to drop correctness? | Yes, especially for unmeasured requirements. | Mandatories, safety and user-provided scope are hard constraints before ranking. | Addressed by design; behavior unproven |
| Won't scoring 1–5 create false precision? | Yes. Ordinal scores + confidence cannot yield calibrated ROI. | Qualitative Focus default, script optional and labeled *heuristic*. | Addressed |
| Will Grill Me questioning slow down users? | It can. A relentless interview is the opposite of a quick MVP loop. | Flash/Focus/Deep; inspect context first; question only high-information blockers. | Addressed by design |
| Can dependency edges trick ranker into skipping prerequisites? | Yes, if treated as separate ranked tasks. | Selected tasks pull transitive dependencies; cycles/missing refs fail validation. | Unit-tested |
| What happens when mandatory work exceeds budget? | Dropping it silently violates requirements. | Ranker exits with explicit conflict. | Unit-tested |
| Does impact/effort greedily maximize portfolio value? | No: it ignores synergy, overlaps and true uncertainty. | Document limitations; human review, no optimization guarantees. | Addressed |
| Does this force a heavy workflow on a one-line fix? | Could happen with always-on rules. | Core says execute trivial specified work directly; AGENTS.md only compact fallback. | Needs runtime eval |
| Does the core secretly depend on a Matt Pocock subskill? | `grill-me` itself often delegates to `grilling`. | Our `references/grill.md` contains the whole method. | Static review passes |
| Do we need a giant multi-agent framework? | Adds complexity and tokens without evidence. | One self-contained skill; no orchestration/runtime dependency. | Addressed |
| Can all agents load these files identically? | No; discovery and command invocation vary. | Canonical spec + CLI + documented manual fallback. | Runtime matrix not fully verified |
| Can we claim empirical savings? | No controlled study has been run for our own skill. | Ship scenarios and test plan, report no measured uplift. | Honest limitation |
| Can dependencies/install scripts be weaponized? | Installers modify user files. | Standard-library-only optional script, no network, dry run, no silent overwrite. | Unit-tested, not externally audited |
| Could adding a license/logo involve infringement? | Copying existing marks creates avoidable risk. | MIT original text; optional original icon, no copied logos. | Addressed |

## Audit verdict

**Fit for a v1 public release with stated limitations.** Scope and safety design are explicit; the skill package has offline checks and reproducible script tests. **Not proven** to improve LLM behavior, trigger correctly in every host, or deliver measured Pareto-like savings. Publish as a transparent open-source method, then gather real before/after evaluations.

## Release checks

- [x] Standard `skills/pareto-forge/SKILL.md` with proper metadata
- [x] Progressive disclosure via focused references
- [x] Separate decision record template
- [x] No external tool required by core workflow
- [x] Installer safety guards and optional offline helper
- [x] Unit tests and GitHub CI config included
- [x] Behavioral eval prompts and scoring rubric included
- [ ] Blind baseline-vs-skill trials on target models (future)
- [ ] End-to-end verification on every agent product (future)
- [ ] Independent security review (future)
