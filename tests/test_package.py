import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PackageContractTest(unittest.TestCase):
    def test_manifests_agree(self):
        plugin = json.loads((ROOT / "plugin.json").read_text())
        marketplace = json.loads((ROOT / "marketplace.json").read_text())
        entry = marketplace["plugins"][0]

        self.assertEqual(plugin["name"], marketplace["name"])
        self.assertEqual(plugin["name"], entry["name"])
        self.assertEqual(plugin["version"], marketplace["metadata"]["version"])
        self.assertEqual(plugin["version"], entry["version"])
        self.assertNotIn("hooks", plugin)
        self.assertEqual(entry["source"], ".")

    def test_customization_frontmatter(self):
        paths = (
            "agents/tzes.agent.md",
            "agents/advisor-plan.agent.md",
            "agents/advisor-review.agent.md",
            "skills/minimal-code/SKILL.md",
            "skills/project-audit/SKILL.md",
        )
        for relative_path in paths:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text()
                frontmatter, body = text.split("---\n", 1)[1].split("\n---\n", 1)
                self.assertIn("description:", frontmatter)
                self.assertTrue(body.strip())

    def test_hook_registration(self):
        self.assertFalse((ROOT / "hooks.json").exists())
        hooks = json.loads((ROOT / "workspace/hooks.json").read_text())
        command = hooks["hooks"]["PreToolUse"][0]["command"]
        self.assertEqual(command, "python3 scripts/approve_risky.py")


if __name__ == "__main__":
    unittest.main()