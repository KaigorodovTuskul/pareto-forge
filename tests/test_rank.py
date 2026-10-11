"""Unit tests for the optional, fully deterministic ranking helper."""
import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "skills/pareto-forge/scripts/rank.py"
spec = importlib.util.spec_from_file_location("rank_skill", FILE)
rankmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rankmod)


def task(id, impact=4, effort=1, confidence=.8, **kwargs):
    return dict(id=id, impact=impact, effort=effort, confidence=confidence, **kwargs)


class RankingTests(unittest.TestCase):
    def test_mandatory_is_included(self):
        data = {"candidates": [task("must", impact=1, effort=2, mandatory=True), task("nice", effort=2)]}
        result = rankmod.rank(data, budget=2)
        self.assertEqual([x["id"] for x in result["selected"]], ["must"])

    def test_dependency_is_included(self):
        data = {"candidates": [task("base", impact=1), task("feature", dependencies=["base"])]}
        selected = [x["id"] for x in rankmod.rank(data, budget=2)["selected"]]
        self.assertEqual(set(selected), {"base", "feature"})

    def test_mandatory_budget_conflict_fails_loudly(self):
        with self.assertRaisesRegex(ValueError, "Mandatory"):
            rankmod.rank({"candidates": [task("must", effort=3, mandatory=True)]}, budget=2)

    def test_cycle_fails(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            rankmod.rank({"candidates": [task("a", dependencies=["b"]), task("b", dependencies=["a"])]})

    def test_duplicate_fails(self):
        with self.assertRaises(ValueError):
            rankmod.rank({"candidates": [task("a"), task("a")]})

    def test_confidence_bounds(self):
        with self.assertRaises(ValueError):
            rankmod.rank({"candidates": [task("a", confidence=1.01)]})

    def test_ineligible_is_excluded(self):
        result = rankmod.rank({"candidates": [task("a", eligible=False), task("b")]})
        self.assertEqual(result["excluded"], ["a"])
        self.assertEqual(result["selected"][0]["id"], "b")

    def test_no_fake_80_guarantee(self):
        result = rankmod.rank({"candidates": [task("a")]})
        self.assertIn("not", result["notice"].lower())

    def test_unknown_dependency_fails(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            rankmod.rank({"candidates": [task("a", dependencies=["b"])]})

    def test_deterministic_tiebreak(self):
        result = rankmod.rank({"candidates": [task("z"), task("a")]})
        self.assertEqual([x["id"] for x in result["selected"]], ["a", "z"])


if __name__ == "__main__":
    unittest.main()
