# Example: Pareto Forge for a web UI

**Request:** “Create a quick interactive visual dashboard with multiple charts.”

**Value:** one launchable page with a usable core interaction, readable data and representative chart families.

**Cut:** defer custom theme engines, multiple frameworks, elaborate state management and optional unit-test infrastructure. Reuse the existing chart/UI library.

**Ship:** put working plots, small sample data and basic navigation in an easily runnable app. Do a smoke check: launch, switch a chart, observe the expected output.

**Stop:** once the main workflow works and nothing critical is broken. Clearly state which enhancements were deferred.

**Scope boundary:** if user requests **all** chart types or contractually specified variants, a partial prototype does not satisfy the request without explicit permission. Speed is not an excuse to misrepresent completeness.
