#!/usr/bin/env python3
"""Minimal offline Agent Skills spec preflight + repository reference validation."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "pareto-forge"


def validate():
    failures = []
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    parts = content.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return ["SKILL.md missing YAML frontmatter"]
    front = parts[1]
    # We constrain our own frontmatter to simple scalar metadata.
    name = re.search(r"(?m)^name:\s*(.+?)\s*$", front)
    desc = re.search(r"(?m)^description:\s*(.+?)\s*$", front)
    if not name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)):
        failures.append("Invalid skill name")
    elif name.group(1) != SKILL.name or len(name.group(1)) > 64:
        failures.append("name must match skill directory and <=64 chars")
    if not desc or not 1 <= len(desc.group(1)) <= 1024:
        failures.append("description must be 1–1024 characters")
    if len(content.splitlines()) > 500:
        failures.append("SKILL.md exceeds 500 lines")
    # Restrict validation to relative Markdown links found in the core skill.
    for raw in re.findall(r"\]\(([^)]+)\)", content):
        if raw.startswith(("https://", "http://", "#")):
            continue
        path = (SKILL / raw.split("#", 1)[0]).resolve()
        if not path.is_relative_to(SKILL.resolve()) or not path.is_file():
            failures.append(f"Broken or unsafe skill reference: {raw}")
    for file in ["README.md", "LICENSE", "docs/RESEARCH.md", "docs/DESIGN_AUDIT.md"]:
        if not (ROOT / file).is_file():
            failures.append(f"Missing repository file: {file}")
    for doc in ROOT.rglob("*.md"):
        if "__pycache__" in doc.parts:
            continue
        for raw in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if raw.startswith(("https://", "http://", "#", "mailto:")):
                continue
            path = (doc.parent / raw.split("#", 1)[0]).resolve()
            if not path.is_relative_to(ROOT.resolve()) or not path.exists():
                failures.append(f"Broken local Markdown link in {doc.relative_to(ROOT)}: {raw}")
    try:
        data = json.loads((ROOT / "tests/evals.json").read_text(encoding="utf-8"))
        cases = data["scenarios"]
        ids = [case["id"] for case in cases]
        if len(ids) != len(set(ids)) or len(ids) < 6 or not all(case.get("prompt") and case.get("must") for case in cases):
            failures.append("Behavioral eval scenarios have missing content or duplicate IDs")
    except (ValueError, KeyError, TypeError) as error:
        failures.append(f"Invalid behavioral evaluation JSON: {error}")
    return failures


if __name__ == "__main__":
    errors = validate()
    if errors:
        print("\n".join("FAIL: " + error for error in errors), file=sys.stderr)
        sys.exit(1)
    print("PASS: offline structure, frontmatter and skill links")
