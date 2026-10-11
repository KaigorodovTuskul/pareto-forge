# Engineering guardrails

Apply for coding, architecture, migrations, automation and refactoring. Inspired by the minimal-change philosophy of Ponytail, independently written.

## Completeness beats line-count vanity

A small diff is valuable only if it preserves behavior, security, accessibility, compatibility and maintainability. A compact implementation with missing tests is *not* the minimal complete solution. Prefer what existing maintainers will understand.

## Decision ladder

1. Is a change necessary to deliver the requested outcome?
2. Can an unnecessary path/feature be removed?
3. Can we reuse the project's existing implementation or interface?
4. Is the required behavior already in the platform / standard library?
5. Can an existing approved dependency be used safely?
6. Only then: add the smallest new module, with tests at critical seams.

For bugs, identify the root cause, affected callers, regression test and needed migration or rollout. For new features, ship a vertical slice with an observable success signal. Check logs/config/fixtures/docs as appropriate; avoid ceremony when not appropriate.

## Reversibility

Prefer feature flags only if rollback cannot be achieved safely otherwise. Always add checkpoints for destructive changes. Do not auto-run destructive commands. For major work, propose staged rollout and monitoring.

## Signals of unnecessary complexity

Speculative settings; premature plugin systems; duplicate abstractions; adding dependencies for tiny operations; long plans without a falsifiable milestone; needless agent-to-agent calls; verbose output that does not change a decision.

## When complexity *is* justified

Regulatory obligations, defense-in-depth security, stable performance, audited provenance, reliability, multi-team interfaces, or demonstrated long-term maintenance savings. Document these reasons; avoid “YAGNI” as an excuse to cut them.
