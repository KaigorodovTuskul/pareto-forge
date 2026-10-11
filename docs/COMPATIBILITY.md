# Compatibility & installation

**Compatibility goal:** portable, vendor-neutral instructions plus practical distribution. **Truthful limitation:** no static archive can guarantee identical behavior on *every agent that exists*, including private/unsupported products. Agent Skills describes a format; each client controls discovery, invocation and permission prompts.

## Preferred path: ecosystem installer

Once this repo is on GitHub, use the [Vercel Labs skills CLI](https://github.com/vercel-labs/skills), which maintains an evolving client registry:

```bash
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge --agent '*'
npx skills add KaigorodovTuskul/pareto-forge --skill pareto-forge -a claude-code -a codex -a cursor
```

`--agent '*'` covers **agents recognized by the installed CLI version**, not every conceivable agent. New/renamed client IDs may change. `-g` installs globally. `--copy` can replace symlink installation if the platform disallows symlinks. Review the installer before use. See its [official supported-agent table](https://github.com/vercel-labs/skills#supported-agents).

## Native discovery: representative agents

| Agent | Project discovery | Global discovery | Confidence |
|---|---|---|---|
| Claude Code | `.claude/skills/pareto-forge/` | `~/.claude/skills/pareto-forge/` | Documented standard convention |
| Codex | `.agents/skills/pareto-forge/` | `~/.agents/skills/pareto-forge/` | Listed in CLI registry |
| Cursor | `.agents/skills/pareto-forge/` | `~/.cursor/skills/pareto-forge/` | Listed in CLI registry |
| Gemini CLI | `.agents/skills/pareto-forge/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` | [Gemini docs](https://geminicli.com/docs/cli/skills/) |
| OpenCode | `.agents/skills/pareto-forge/` or `.opencode/skills/` | `~/.agents/skills/` or `~/.config/opencode/skills/` | [OpenCode docs](https://docs.opencode.ai/docs/skills/) |
| GitHub Copilot | `.agents/skills/pareto-forge/` or `.github/skills/` | `~/.agents/skills/` or `~/.copilot/skills/` | [GitHub docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| Cline | `.agents/skills/pareto-forge/` | `~/.agents/skills/pareto-forge/` | Listed in CLI registry |
| Antigravity | `.agents/skills/pareto-forge/` | `~/.gemini/antigravity/skills/` | Listed in CLI registry |
| Continue | `.continue/skills/pareto-forge/` | `~/.continue/skills/pareto-forge/` | Listed in CLI registry |
| Goose | `.goose/skills/pareto-forge/` | `~/.config/goose/skills/` | Listed in CLI registry |
| OpenClaw | `skills/pareto-forge/` | `~/.openclaw/skills/pareto-forge/` | Listed in CLI registry |
| Windsurf | Let `npx skills` select its current path | Let `npx skills` select its current path | Ecosystem installer, not host-tested |
| Roo Code and other implementations | Check current host docs / CLI registry | Check current host docs / CLI registry | Manual adapter unverified |

A *discovered* skill is not necessarily *automatically invoked*. The host may ask for approval, require skill activation or have differing filename/path conventions. No integrations are required in the core skill: it is Markdown plus optional Python scripts.

## Offline installer

`python scripts/install.py` copies the canonical folder from a checkout. It supports a documented shortlist and uses **project-local `.agents/skills/`** by default. Use `--dry-run` before `--all`, especially in an existing workspace. Existing skill folders are protected unless `--force` is explicit. No files outside `pareto-forge` skill directories are overwritten; no remote commands are fetched.

This installer includes `roocode` as a **best-effort local path**, not an independently verified official adapter. For that client prefer current vendor docs.

## Unsupported agents / legacy clients

1. Check whether it supports the standard [Agent Skills](https://agentskills.io/specification) folder.
2. Otherwise paste or reference [`SKILL.md`](../skills/pareto-forge/SKILL.md) in that client's custom instruction system.
3. If it only reads root-level instructions, adapt the compact [`AGENTS.md`](../AGENTS.md), respecting existing project-specific rules.
4. If there is no instruction mechanism, the skill cannot be installed natively; use a supported client instead.

**Avoid** scattering duplicate skill files across paths in the *same* workspace. Depending on the host, duplicates may cause repeated activation. Use the registry installer or only the needed manual path.

## Tested vs untested

Included in repo: structural validation, Python ranking unit tests, copy-install tests, CI workflow. **Not included:** live end-to-end tests against each proprietary AI client, model prompting/obedience benchmarks, or verification of host auto-activation. Those are future integration checks, not implicit promises.
