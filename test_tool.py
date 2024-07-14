import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent


class CommandBehavior(unittest.TestCase):
    def run_tool(self, *args, stdin=None):
        return subprocess.run([sys.executable, str(ROOT / "tool.py"), *args],
                              input=stdin, capture_output=True, text=True, timeout=10)

    def test_documented_example(self):
        result = self.run_tool(str(ROOT / "examples" / "input.json"))
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = json.loads((ROOT / "examples" / "expected.json").read_text())
        self.assertEqual(json.loads(result.stdout), expected)

    def test_stdin_matches_file_input(self):
        example = (ROOT / "examples" / "input.json").read_text()
        result = self.run_tool("-", stdin=example)
        expected = json.loads((ROOT / "examples" / "expected.json").read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)

    def test_rejects_non_object_without_result(self):
        result = self.run_tool("-", stdin="null")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("JSON object", result.stderr)

    def test_rejects_non_finite_input(self):
        result = self.run_tool("-", stdin='{"value": NaN}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("finite", result.stderr)


if __name__ == "__main__":
    unittest.main()
