from pathlib import Path
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class QualityGateContractTests(unittest.TestCase):
    def test_workbench_renders_authoritative_local_market_facts(self):
        for phrase in (
            "不得由模型手工计算汇总数字",
            "工作台确定性质量门",
            "确定性事实文件",
            "公开报告不得出现内部工具名称",
        ):
            self.assertIn(phrase, SKILL)


if __name__ == "__main__":
    unittest.main()
