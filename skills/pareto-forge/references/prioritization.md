# Prioritization protocol

Read when choices genuinely compete for limited time or resources.

## Evidence hierarchy

1. Measured effects in relevant context (with provenance, time period, limitations).
2. Controlled experiments, reproduced results, recent user evidence.
3. Reasoned estimates with explicit assumptions and uncertainty.
4. Intuition: acceptable for cheap, reversible experiments, not as a confident ROI claim.

## Hard gates before scoring

Write mandatory obligations, safety/correctness requirements, dependencies, deadline constraints and reversible versus irreversible options. A high numerical score never overrides a hard gate. Distinguish regulatory/contractual must-haves from discretionary work. Don't optimize a single proxy metric at the expense of the outcome.

## Scoring as a conversation aid

For small tradeoffs, use qualitative high/medium/low. For >5 comparable options with usable estimates, the bundled optional script ranks eligible choices by:

`heuristic_score = impact * confidence / effort`

Here impact and effort are 1–5 ordinal estimates; confidence is a subjective fraction 0–1. This is **not** an expected-value model with validated units and cannot prove ROI. Add `mandatory` and `dependencies` in JSON when relevant. Ranking cannot guarantee the optimal portfolio; think critically about overlap, opportunity cost and interactions. Never invent a false precision.

## A better selection loop

1. Find the **binding constraint** on outcome (e.g. distribution, data trust, latency, onboarding, cycle time).
2. List at least one way to *remove* work, not just add features.
3. Separate required foundations from optional enhancements.
4. Select the cheapest experiment that could invalidate the top choice.
5. Commit to a minimum valuable slice, with explicit non-goals and upgrade triggers.
6. Revisit rankings when conditions or measured outcomes change.

## Edge cases

- **One clear requirement:** skip ranking and execute.
- **Equal score, different risk:** prefer lower irreversible downside.
- **Poor estimates:** label uncertainty, prefer information-gathering experiments over scoring.
- **Strong dependencies:** prerequisite tasks may have low direct impact but still be necessary.
- **Complementary tasks:** evaluate bundles; a greedy score may miss synergy.
- **Reused infrastructure:** compare total ownership cost, not just code length.
- **Two unrelated objectives:** ask user which objective has priority, or present separate Pareto frontiers.

## Practical decision table

| Option | Outcome contribution | Evidence | Effort/maintenance | Risk | Verdict |
|---|---|---|---|---|---|
| Small pilot | High if hypothesis true | Medium | Low | Reversible | **Now: test** |
| Full build | Unknown | Low | High | Hard to undo | **Not now** |
| Reuse existing workflow | Medium | High | Very low | Low | **Now** |
