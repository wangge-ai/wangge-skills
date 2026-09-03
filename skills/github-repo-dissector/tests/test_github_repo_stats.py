import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "github_repo_stats.py"
SPEC = importlib.util.spec_from_file_location("github_repo_stats", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ParseRepoTests(unittest.TestCase):
    def test_accepts_owner_repo_and_github_url(self):
        self.assertEqual(MODULE.parse_repo("wangge-ai/wangge-skills"), ("wangge-ai", "wangge-skills"))
        self.assertEqual(
            MODULE.parse_repo("https://github.com/wangge-ai/wangge-skills.git"),
            ("wangge-ai", "wangge-skills"),
        )

    def test_rejects_non_github_or_ambiguous_urls(self):
        credential_url = "https://" + "user:pass@" + "github.com/wangge-ai/wangge-skills"
        for value in (
            "https://example.com/wangge-ai/wangge-skills",
            "https://github.com/wangge-ai/wangge-skills/issues",
            credential_url,
        ):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                MODULE.parse_repo(value)


if __name__ == "__main__":
    unittest.main()
