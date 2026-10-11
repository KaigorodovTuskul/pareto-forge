# Pareto Forge — compact fallback instructions

This file is a fallback for agents that read `AGENTS.md` but do not automatically discover Agent Skills. The canonical skill is [`skills/pareto-forge/SKILL.md`](skills/pareto-forge/SKILL.md). **Do not treat this as a replacement for existing project-specific requirements.**

On non-trivial prioritization, planning, coding or architecture tasks:
1. Define the user outcome, observable success and hard constraints first.
2. Compare a few substantially different approaches, including remove/reuse/do less; choose the highest-leverage *feasible* slice and name what is deferred.
3. Challenge the most consequential assumption with a cheap falsification test; ask a question only when genuinely blocking.
4. For implementation, favor no change → deletion → existing code → platform → installed dependency → smallest complete new code.
5. Verify observed results and report what was and was not checked. Never claim empirical 80/20 effects or test success without evidence.

Use **Flash** for trivial reversible tasks (just do them), **Focus** by default and **Deep** for high-stakes decisions. Never optimize away security, correctness, access control, privacy, legal obligations, user-mandated scope or required tests. No irreversible actions without authorization.
