# Challenge / grilling protocol

A *self-contained* adversarial design review inspired by the questioning approach in mattpocock/skills. This file does **not** call or require an external `grilling` skill.

## Depth control

- **Flash:** no grill unless an obvious safety/logic hole appears.
- **Focus:** ask yourself five questions; share the top 1–3 unresolved ones only.
- **Deep:** build a decision tree. Identify dependencies, attack the riskiest nodes, record outcomes and unresolved questions. Interrogate **decisions**, not people.

## Procedure

1. Write the decision being made in one sentence and its one-sentence purpose.
2. Locate answered facts in existing code, docs, data and conversation. Never ask for readily discoverable information.
3. Build a small branch map: goal → options → assumptions → failure modes → checks.
4. Try a **premortem**: “Three months later this failed. Why?”
5. Ask the highest-information unresolved question with your recommended answer; batch only when user explicitly prefers a questionnaire. Do not demand confirmation for routine reversible work.
6. If user input is unavailable and risk is modest, proceed using a labeled reversible assumption. If risk is severe, stop only the unsafe step, and present the safe next step.
7. Capture decisions and explicit reasons for rejecting alternatives; reopen only on new evidence.

## Seven useful attacks (choose sparingly)

- Are we optimizing for the real outcome, or a convenient proxy?
- Does the chosen solution survive a hostile but realistic edge case?
- What must be true about the data/people/system for this to work?
- Which cost shows up after launch rather than during coding?
- Does eliminating the feature solve the user's problem better?
- What is the earliest observable signal that we are wrong?
- What would a skeptical reviewer ask us to reproduce?

## Rules

- **One decision per question**, recommend a default and articulate tradeoffs.
- Prefer experiments and observation over extended debate.
- No fake confidence, no open-ended “let's discuss everything” loops.
- No adversarial review theater for low-risk work.
- Report the strongest counterargument fairly, even if the preferred option survives.

## Output in Deep mode

**Decision:** …
**Supported facts:** …
**Main hypothesis:** …
**Best alternative:** …
**Strongest objection:** …
**Cheap falsification test:** …
**Owner / next review:** …
