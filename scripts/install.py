#!/usr/bin/env python3
"""Install Pareto Forge locally without dependencies. Other agents: npx skills add."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "pareto-forge"
# Keep this a *documented shortlist*, not a claim to represent every agent.
PROJECT_PATHS = {
    "universal": ".agents/skills",
    "claude-code": ".claude/skills",
    "codex": ".agents/skills",
    "cursor": ".agents/skills",
    "github-copilot": ".agents/skills",
    "gemini-cli": ".agents/skills",
    "opencode": ".opencode/skills",
    "cline": ".agents/skills",
    "windsurf": ".agents/skills",
    "continue": ".continue/skills",
    "goose": ".goose/skills",
    "roocode": ".roo/skills",
    "openclaw": "skills",
    "antigravity": ".agents/skills",
}
GLOBAL_PATHS = {
    "universal": ".agents/skills",
    "claude-code": ".claude/skills",
    "codex": ".agents/skills",
    "cursor": ".cursor/skills",
    "github-copilot": ".copilot/skills",
    "gemini-cli": ".gemini/skills",
    "opencode": ".config/opencode/skills",
    "cline": ".agents/skills",
    "windsurf": ".agents/skills",
    "continue": ".continue/skills",
    "goose": ".config/goose/skills",
    "roocode": ".roo/skills",
    "openclaw": ".openclaw/skills",
    "antigravity": ".gemini/antigravity/skills",
}


def install(target, agents, global_scope=False, force=False, dry_run=False):
    mapping = GLOBAL_PATHS if global_scope else PROJECT_PATHS
    folders = sorted({(target / mapping[a] / "pareto-forge").resolve() for a in agents})
    operations = []
    source_status = []
    for dest in folders:
        if dest == SOURCE.resolve():
            source_status.append((str(dest), "source-present"))
            continue  # Never delete or overwrite the canonical source folder.
        if dest.exists() and not force:
            raise FileExistsError(f"{dest} already exists; omit target, or pass --force to replace this skill directory")
        operations.append(dest)
    if dry_run:
        return source_status + [(str(dest), "dry-run") for dest in operations]
    for dest in operations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if not dest.is_dir() or dest.is_symlink():
                raise ValueError(f"Refusing to replace non-directory/symlink: {dest}")
            shutil.rmtree(dest)
        shutil.copytree(SOURCE, dest)
    return source_status + [(str(dest), "installed") for dest in operations]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", "-a", action="append", choices=sorted(PROJECT_PATHS), default=None,
                        help="Agent ID; repeat to install multiple (default: universal)")
    parser.add_argument("--all", action="store_true", help="All agents in this local installer's shortlist")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="Install for current user")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Workspace destination for project scope")
    parser.add_argument("--force", action="store_true", help="Replace ONLY existing pareto-forge skill directories")
    parser.add_argument("--dry-run", action="store_true", help="Print targets without writing")
    args = parser.parse_args(argv)
    agents = list(PROJECT_PATHS) if args.all else (args.agent or ["universal"])
    target = Path.home() if args.global_scope else args.project.expanduser().resolve()
    try:
        for dest, status in install(target, agents, args.global_scope, args.force, args.dry_run):
            print(f"{status}: {dest}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
