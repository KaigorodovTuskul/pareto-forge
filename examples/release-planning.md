# Example: Ship a useful onboarding slice this week

**Request:** “We have 15 potential enhancements and five days to ship onboarding.”

**Must-have:** users can accept invitations and sign in with correct access permissions and required accessibility; existing API behavior remains valid.

**Do now:** reuse the invitation API and existing UI; support the common happy path plus essential errors. Check the invitation flow and a denied-permission path, then ship.

**Not now:** new orchestration service, complex approval configuration, animations and exhaustive analytics. Don't write a long architecture RFC for a reversible short release.

**Stop:** once a new teammate can complete onboarding and mandatory permissions are correct. If the user later needs cross-organization roles or advanced audits, plan the next increment then. No unmeasured promise of an 80% uplift.
