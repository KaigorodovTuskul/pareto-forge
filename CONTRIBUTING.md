# Contributing to Pareto Forge

Prefer **subtracting complexity** to accumulating prompt rules.

1. Start with a reproducible failure: scenario, environment/model, expected behavior and observed behavior.
2. Add or adjust a case in `tests/evals.json` for behavior, or a Python unit test for executable helpers.
3. Change the smallest instruction/reference that fixes the problem; avoid expanding `SKILL.md` unless activation-level behavior really changes.
4. Run `python scripts/validate.py`, `python -m unittest discover -s tests -v`, and `python -m unittest discover -s benchmark/tests -v`.
5. If claiming performance improvements, follow the frozen [`benchmark/PROTOCOL.md`](benchmark/PROTOCOL.md) and attach audited, anonymized A/B/C evidence. Do not alter the task corpus or independent graders after observing results; avoid cherry-picking.
6. Confirm changes preserve security and user-required scope. Keep all third-party code out unless license and attribution are checked.

## PR guide

State: **problem / candidate fix / alternatives considered / observed test result / new costs**. Keep requests focused. Discuss breaking behavioral changes in an issue first.
