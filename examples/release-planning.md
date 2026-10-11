# Example: Release planning under a deadline

**Intent:** a team has 15 candidate enhancements and five days to ship a reliable onboarding release.

## Outcome and constraints

New employees complete an accessible, auditable invitation and onboarding flow. Mandatory: least-privilege access, existing API compatibility, the team's localization requirement, and a working rollback path.

## Compare paths

1. **Replace the workflow engine:** powerful but introduces high integration risk.
2. **Reuse the invitation API and improve the onboarding checklist:** small, testable vertical slice.
3. **Skip onboarding changes:** least effort but unlikely to satisfy the release goal.

## Challenge

Would the slimmed-down design still work for users with multiple teams, expired invitations, and delayed approvals? Verify on real test accounts before declaring the pilot sufficient.

## Smallest safe delivery

Prefer option 2 *if* its integration tests and accessibility checks pass. Defer dashboard widgets, custom rule builders, and speculative integrations. Keep security and audit requirements intact.

## Evidence, not claims

Run user scenarios and failure-injection tests; report observed completion rate, defects and recovery time. No assertion that the selected work provides 80% of value until evaluated.
