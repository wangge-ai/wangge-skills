import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"


class RepositoryContractTests(unittest.TestCase):
    def test_catalog_matches_skill_directories(self):
        catalog = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
        catalog_names = {item["name"] for item in catalog["skills"]}
        directory_names = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(catalog_names, directory_names)

    def test_every_skill_has_public_package_files(self):
        for skill_dir in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
            with self.subTest(skill=skill_dir.name):
                for relative in ("SKILL.md", "README.md", "LICENSE", "agents/openai.yaml"):
                    self.assertTrue((skill_dir / relative).is_file(), f"missing {relative}")
                skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
                name_match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", skill_text)
                self.assertIsNotNone(name_match)
                self.assertEqual(name_match.group(1), skill_dir.name)

    def test_markdown_relative_links_resolve(self):
        link_pattern = re.compile(
            r"\[[^\]]*\]\(([^)]+)\)|`((?:references|scripts|examples)/[^`]+|(?:social|wechat)-[^`]+\.md)`"
        )
        missing = []
        for markdown in ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8-sig")
            for match in link_pattern.finditer(text):
                target = match.group(1) or match.group(2)
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = target.split("#", 1)[0]
                if target and not (markdown.parent / target).exists():
                    missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [])

    def test_public_tree_has_no_known_private_brand_residue(self):
        forbidden = ("沃朗森", "wolongsen", "AI应用实战派PRO", "AI罗盘指北针", "你旺哥")
        hits = []
        for path in ROOT.rglob("*"):
            if path == Path(__file__).resolve():
                continue
            if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in {".md", ".py", ".json", ".yaml", ".yml", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8-sig")
            for value in forbidden:
                if value.lower() in text.lower():
                    hits.append(f"{path.relative_to(ROOT)}: {value}")
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
