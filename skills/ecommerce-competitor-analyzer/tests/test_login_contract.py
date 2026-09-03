from pathlib import Path
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")
REPORT_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "references" / "report-template.md"
).read_text(encoding="utf-8")


class LoginContractTests(unittest.TestCase):
    def test_requires_selected_platforms_and_independent_login_preflight(self):
        for phrase in (
            "不默认扩展为“全平台”",
            "最小业务可用性预检",
            "首页没有昵称、个人中心或订单入口，不能单独作为未登录证据",
            "标签页指针、当前 URL 或平台域名不一致属于线路错误",
            "可继续的平台立即进入业务采集",
            "整体才写 `waiting_login`",
            "其他平台等待登录时，整体写 `partial`",
            "有效样本为 0 时不得写 `partial`",
        ):
            self.assertIn(phrase, SKILL)
        self.assertNotIn("本轮不开始业务采集", SKILL)

    def test_forbids_credentials_and_login_bypass(self):
        for phrase in ("账号", "密码", "Cookie", "Token", "不自动登录", "不绕过验证码"):
            self.assertIn(phrase, SKILL)

    def test_report_keeps_available_platform_results(self):
        for phrase in (
            "不得只输出登录预检受阻报告",
            "可继续的平台已有样本、其他平台等待登录时",
            "种子链接所属平台可继续时必须读取种子商品",
        ):
            self.assertIn(phrase, REPORT_TEMPLATE)

    def test_live_market_outputs_are_owned_by_the_workbench_quality_gate(self):
        for phrase in (
            "`competitor_evidence.csv`",
            "`collection_evidence_manifest.json`",
            "`analysis_notes.json`",
            "`evidence/raw/`",
            "不得由模型手工计算汇总数字",
            "最终 `success` 由工作台确定性质量门决定",
            "公开报告不得出现内部工具名称",
        ):
            self.assertIn(phrase, SKILL)
        self.assertIn("所有数量和价格统计只从确定性事实文件渲染", REPORT_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
