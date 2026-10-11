# Engineering: fastest safe useful slice

Read only if implementing code. Inspired by the pragmatic minimalism of Ponytail; this text is original.

## Implementation ladder

1. Is anything required beyond a direct edit or simple answer? If not, do it.
2. Reuse existing code or native platform features before adding a dependency.
3. Implement one usable vertical slice without speculative abstraction.
4. Check the **cheapest meaningful proof** that the requested result works.
5. Stop. Further polish belongs on a "later" list, not in the critical path.

## Proportionate checks, not a blanket ban on tests

- One-off visual demo: launch it, exercise primary navigation and inspect one representative chart. Don't create CI and dozens of tests without reason.
- Small pure function: run a few edge cases; existing unit tests may be cheaper than manual inspection.
- Permission, payment, privacy, migration, durable storage, or production dependency: relevant automated tests and safeguards are part of the **minimum usable** result. Never remove them to save time.
- Existing project requirements: run the mandated checks; don't change an explicit Definition of Done unilaterally.

## Stop conditions

Stop at *usable + must-haves + proportionate check*. Don't refactor working code solely for beauty or future needs. Record noncritical compromises clearly. If a mandatory requirement remains unmet, do not declare the task complete: ask to narrow scope or finish the requirement.

## Avoid

Large plan documents for small work; needless agents and tools; generalized plugin architectures; theme engines for demos; README dissertations; dependency installation for a trivial helper; testing the framework instead of the delivered feature; rewriting unrelated code.

## Escalate when justified

Large-scale changes, unknown security risks, irreversible state mutations, heavily coupled architecture, poor observability or ambiguous binding acceptance criteria justify targeted research, rollback plans and deeper checks.
