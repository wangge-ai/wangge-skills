from pathlib import Path
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class LoginContractTests(unittest.TestCase):
    def test_requires_one_platform_and_login_preflight(self):
        for phrase in (
            "明确选择当前链接所属的平台",
            "不默认扩展为“全平台”",
            "最小业务可用性预检",
            "不能只因首页没有昵称、个人中心或订单入口就判定未登录",
            "标签页指针、当前 URL 或平台域名不一致属于线路错误",
            "直接返回 `waiting_login`",
            "均为 0 时",
        ):
            self.assertIn(phrase, SKILL)

    def test_saved_html_bypasses_login(self):
        self.assertIn("`--html-file` 本地保存页面不要求平台登录", SKILL)

    def test_workbench_uses_manifest_for_counts_and_status(self):
        for phrase in (
            "不得由模型手工计算汇总数字",
            "工作台确定性质量门",
            "manifest 和实际文件",
            "公开报告不得出现内部工具名称",
        ):
            self.assertIn(phrase, SKILL)

    def test_workbench_reuses_current_browser_without_a_playwright_fallback_window(self):
        for phrase in (
            "`--use-current-browser`",
            "复用当前可见浏览器",
            "`not_available`",
            "不会再打开另一套 Playwright 浏览器窗口",
            "不要保存登录页、动态二维码、手机号或账号输入框截图",
        ):
            self.assertIn(phrase, SKILL)


if __name__ == "__main__":
    unittest.main()
