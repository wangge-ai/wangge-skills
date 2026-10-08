from pathlib import Path
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class LoginContractTests(unittest.TestCase):
    def test_requires_one_platform_and_login_preflight(self):
        for phrase in (
            "明确选择一个平台",
            "不默认使用“全平台”",
            "最小业务可用性预检",
            "不能只因首页没有昵称、个人中心或订单入口就判定未登录",
            "标签页指针、当前 URL 或平台域名不一致属于线路错误",
            "返回 `waiting_login`",
            "有效商品样本为 0 时",
        ):
            self.assertIn(phrase, SKILL)

    def test_local_evidence_bypasses_login(self):
        self.assertIn("保存 HTML 或已授权浏览器导出的结构化 JSON 是本地证据", SKILL)

    def test_market_upstream_contract_defers_counts_and_success(self):
        for phrase in (
            "作为实时市场分析的上游",
            "`competitor_evidence.csv`",
            "`collection_evidence_manifest.json`",
            "`evidence/raw/`",
            "不得由模型手工计算汇总数字",
            "最终 `success` 由工作台确定性质量门决定",
            "公开报告不得出现内部工具名称",
        ):
            self.assertIn(phrase, SKILL)


if __name__ == "__main__":
    unittest.main()
