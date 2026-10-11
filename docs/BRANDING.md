# Branding — Pareto Forge

## Current assets

The official repo README uses an original, user-approved logo built around an anvil-like silhouette and a cyan convergence point. The artwork is also adapted for legibility in GitHub's light and dark color themes.

| Asset | Purpose |
|---|---|
| [`assets/pareto-forge-logo.png`](assets/pareto-forge-logo.png) | Canonical transparent logo, 640 × 640 PNG, shown on light backgrounds |
| [`assets/pareto-forge-logo-on-dark.png`](assets/pareto-forge-logo-on-dark.png) | High-contrast derivative for GitHub dark mode |
| [`assets/workflow.svg`](assets/workflow.svg) | Repo-specific documentation diagram for the five decision gates |

All assets are referenced with **relative paths**, so they work after the repository is renamed or forked. The README uses `<picture>` with `(prefers-color-scheme: dark)` to select the high-contrast variation.

## Usage

- Keep the icon recognizable and generously spaced.
- Keep the focal point electric cyan; avoid unrelated accent colors.
- Never use the mark to imply association with the projects referenced in the skill research.
- Check readability in GitHub light/dark mode and when reduced to 32 px.
- Do not ship fonts, third-party company logos, or generated-image drafts in releases.
- The original generated artwork is included as a resized transparent PNG. The high-contrast rendition is a color-visibility derivative, **not** an original hand-drawn vector trace.

## Optional vector variant

If you later create a clean manual vector trace, save it as `docs/assets/pareto-forge-logo.svg`. Inspect its contents before publishing; SVG should be static (no scripts, external links, remote content or embedded fonts). Do not rename PNG bytes to `.svg`.

## Brand versus source license

Source code and documentation are distributed under MIT unless otherwise stated. A source license does not automatically grant rights to impersonate the project's identity or claim endorsement. Consider a separate trademark policy if the brand develops beyond a hobby project.
