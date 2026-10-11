#!/usr/bin/env python3
"""Deterministic *heuristic* candidate ranking; no APIs, packages or side effects.

This script is optional: use only for several comparable candidates. It does not
replace evidence, constraint review or thinking about complementary work.
"""
import argparse
import json
import math
import sys
from pathlib import Path


def validate(data):
    if not isinstance(data, dict) or not isinstance(data.get("candidates"), list):
        raise ValueError("Expected object with 'candidates' list")
    result = {}
    for i, raw in enumerate(data["candidates"]):
        if not isinstance(raw, dict):
            raise ValueError(f"Candidate {i} must be an object")
        name = raw.get("id")
        if not isinstance(name, str) or not name or name in result:
            raise ValueError(f"Candidate {i} needs a unique non-empty string id")
        for field in ("impact", "effort", "confidence"):
            value = raw.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name}.{field} must be a finite number")
            minimum, maximum = (0, 1) if field == "confidence" else (1, 5)
            if not minimum <= value <= maximum:
                raise ValueError(f"{name}.{field} must be between {minimum} and {maximum}")
        for field in ("mandatory", "eligible"):
            if field in raw and not isinstance(raw[field], bool):
                raise ValueError(f"{name}.{field} must be boolean")
        deps = raw.get("dependencies", [])
        if not isinstance(deps, list) or len(deps) != len(set(map(str, deps))) or any(not isinstance(d, str) for d in deps):
            raise ValueError(f"{name}.dependencies must be a list of unique string IDs")
        result[name] = dict(raw, dependencies=deps, mandatory=raw.get("mandatory", False), eligible=raw.get("eligible", True))
    for name, item in result.items():
        if item["mandatory"] and not item["eligible"]:
            raise ValueError(f"Mandatory item {name!r} cannot be ineligible")
        for dep in item["dependencies"]:
            if dep not in result:
                raise ValueError(f"{name} has unknown dependency {dep!r}")
            if not result[dep]["eligible"]:
                raise ValueError(f"{name} requires ineligible dependency {dep!r}")
    visiting, visited = set(), set()

    def check(node):
        if node in visiting:
            raise ValueError(f"Dependency cycle involving {node!r}")
        if node in visited:
            return
        visiting.add(node)
        for dep in result[node]["dependencies"]:
            check(dep)
        visiting.remove(node)
        visited.add(node)

    for name in result:
        check(name)
    return result


def closure(name, items):
    answer = set()

    def walk(cur):
        if cur in answer:
            return
        answer.add(cur)
        for d in items[cur]["dependencies"]:
            walk(d)

    walk(name)
    return answer


def score(item):
    return round(item["impact"] * item["confidence"] / item["effort"], 4)


def rank(data, budget=None):
    items = validate(data)
    if budget is not None and (not isinstance(budget, (int, float)) or budget < 0 or not math.isfinite(budget)):
        raise ValueError("budget must be a finite non-negative number")
    compulsory = set()
    for name, item in items.items():
        if item["mandatory"]:
            compulsory.update(closure(name, items))
    cost = lambda selected: sum(items[n]["effort"] for n in selected)
    if budget is not None and cost(compulsory) > budget:
        raise ValueError(f"Mandatory items and prerequisites cost {cost(compulsory):g}, above budget {budget:g}; revise the constraint, not the mandatory items")
    chosen = set(compulsory)
    ranked = sorted(
        (name for name, item in items.items() if item["eligible"] and name not in chosen),
        key=lambda n: (-score(items[n]), n),
    )
    # Greedy heuristic, not an exact knapsack or synergy optimizer.
    for name in ranked:
        group = closure(name, items)
        if budget is None or cost(chosen | group) <= budget:
            chosen.update(group)
    selected = sorted(chosen, key=lambda n: (-score(items[n]), n))
    deferred = sorted((n for n in items if n not in chosen and items[n]["eligible"]), key=lambda n: (-score(items[n]), n))
    excluded = sorted(n for n in items if not items[n]["eligible"])
    return {
        "notice": "Heuristic priority only. Scores are not measured ROI or an 80/20 guarantee.",
        "budget": budget,
        "total_effort": cost(chosen),
        "selected": [{"id": n, "score": score(items[n]), "mandatory": items[n]["mandatory"]} for n in selected],
        "deferred": [{"id": n, "score": score(items[n])} for n in deferred],
        "excluded": excluded,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON file, or '-' for stdin")
    parser.add_argument("--budget", type=float, default=None, help="Optional maximum sum of effort points")
    parser.add_argument("--output", help="Optional JSON destination; defaults to stdout")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        data = rank(json.loads(raw), args.budget)
        result = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"pareto-forge: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
