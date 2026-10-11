import importlib.util
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "scripts/install.py"
spec = importlib.util.spec_from_file_location("installer", SOURCE)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_install_universal_and_claude(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = installer.install(root, ["universal", "claude-code"])
            self.assertEqual(len(result), 2)
            for dest, status in result:
                self.assertTrue((Path(dest) / "SKILL.md").exists())
                self.assertEqual(status, "installed")

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            installer.install(root, ["universal"], dry_run=True)
            self.assertFalse((root / ".agents").exists())

    def test_no_silent_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            installer.install(root, ["universal"])
            with self.assertRaises(FileExistsError):
                installer.install(root, ["universal"])

    def test_does_not_replace_canonical_source(self):
        result = installer.install(installer.ROOT, ["openclaw"], force=True)
        self.assertEqual(result[0][1], "source-present")
        self.assertTrue((installer.SOURCE / "SKILL.md").exists())

    def test_shared_target_deduplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(len(installer.install(Path(folder), ["cursor", "codex", "universal"])), 1)


if __name__ == "__main__":
    unittest.main()
