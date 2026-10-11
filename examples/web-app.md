# Example: product feature prioritization

**Request:** "We need dashboard themes, CSV export, role-based permissions, three chart libraries, and a new sidebar before launch."

**Outcome:** launch an auditable analytics dashboard for a pilot group with correct data access.

**Hard constraints:** role-based restrictions if sensitive data is exposed; security tests. Those cannot be deferred merely because implementation is hard.

**Leverage:** reuse the existing chart library, add a minimal CSV export only if pilot users require it, and ship core visualizations with correct access. Defer redundant charts and multiple themes until there is evidence of value.

**Grill:** who needs CSV in the first week? What happens if export bypasses role checks? Is a new sidebar actually necessary for navigation?

**Implementation:** one narrow slice, existing components, permissions tested, no speculative plugin system.

**Verify:** pilot users can complete the three essential tasks; unauthorized users cannot access or export restricted data; test suite passes.
