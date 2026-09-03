import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_market_html_report.py"
SPEC = importlib.util.spec_from_file_location("render_market_html_report", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DeepReportRenderingTests(unittest.TestCase):
    def test_renders_orchestrated_report_and_emits_valid_markdown_contract(self):
        profile = {
            "row_count": 80,
            "price_summary": {"median": 21.38},
            "sales_summary": {"median": 10000},
            "price_bands": [],
            "price_label_counts": [],
            "top_shops": [],
            "claim_counts": [],
        }
        facts = {
            "field_coverage": {},
            "ad_summary": {},
            "duplicate_summary": {},
            "title_phrases": [],
            "facts": [],
            "deep_analysis": {
                "source_inventory": [],
                "business_price_bands": [],
                "ad_comparison": [],
                "claim_taxonomy": [],
                "claim_cooccurrence": [],
                "brand_map": [],
                "wolongsen_skus": [],
                "competitor_matrix": [],
                "image_diagnostics": [],
            },
        }
        report = {
            "task_card": {
                "decision_goal": "决定沃朗森30–50元牙膏的SKU收敛与验证路径",
                "report_type": "决策型",
                "business_object": "牙膏市场、竞品与内容视觉",
                "reader": "负责人、运营、商品与视觉团队",
                "time_scope": "2026-07-20登录态搜索样本",
                "main_task": "决策型及沃朗森30–50元牙膏定位",
                "submodules": "洞察型供给结构；比较型前10竞品；评估型6张首屏图",
            },
            "evidence_audit": {
                "available": ["80个固定样本"],
                "missing": ["评价正文0条"],
                "conflicts": ["搜索价与详情价必须分口径"],
                "boundaries": ["不推断全平台市场份额"],
            },
            "analysis_plan": {
                "models": ["MECE供给结构", "统一口径基准对标", "决策矩阵"],
                "data_methods": ["确定性事实统计", "图片内容编码"],
                "steps": ["审计证据", "形成条件动作"],
                "depth": "深度报告",
                "directory": ["执行摘要", "关键发现", "行动建议"],
                "can_answer": ["目标价格带是否为空白机会"],
                "cannot_answer": ["真实转化率"],
                "confidence": "供给结构较高，用户需求不形成结论",
                "outputs": ["HTML深度报告", "Markdown报告"],
            },
            "generation": {"status": "绿色", "handling": "自动生成", "confirmation": "用户已确认执行"},
            "executive_summary": {
                "conclusion": "目标价格带不是空白机会。",
                "basis": "目标带13/80，沃朗森占7/13。",
                "action": "先收敛SKU，再做单变量测试。",
                "confidence": "中等",
                "limitation": "评价正文为0。",
            },
            "scope": ["仅覆盖固定搜索样本"],
            "methods": ["MECE对应价格、品牌和卖点结构"],
            "findings": [{
                "title": "目标价格带不是空白机会",
                "fact": "目标带13/80。",
                "evidence": "FACT_TARGET_BAND",
                "explanation": "进入需要依靠差异化而不是跟随定价。",
                "boundary": "不代表全平台市场份额。",
                "evidence_ids": ["FACT_TARGET_BAND"],
            }],
            "mechanisms": [{
                "title": "内部竞争机制",
                "status": "分析推断",
                "analysis": "同价同词可能造成潜在内部竞争，仍需归因数据验证。",
                "evidence_ids": ["FACT_WOLONGSEN_SHELF"],
            }],
            "conclusions": [{
                "type": "确定结论",
                "statement": "当前先做SKU收敛。",
                "evidence_ids": ["FACT_TARGET_BAND"],
            }],
            "actions": [{
                "action": "收敛同价SKU",
                "basis": "发现一",
                "priority": "高",
                "owner": "运营与商品",
                "time": "第1–2天",
                "metric": "同价同词SKU数",
                "risk": "误伤有效链接",
                "fallback": "先暂停投放，不直接下架",
            }],
            "risks": ["评价正文缺失，不能输出VOC结论。"],
            "appendix": ["FACT_*为机器证据编号。"],
            "quality_review": {"score": 92, "result": "通过"},
        }

        html = MODULE.build_html(profile, "编排报告", facts, None, report)
        markdown = MODULE.build_analysis_markdown(report, "编排报告")

        for phrase in (
            "报告任务识别",
            "资料审计",
            "分析方案",
            "生成状态",
            "执行摘要",
            "任务与分析范围",
            "数据与方法",
            "原因或机制分析",
            "行动建议",
            "风险与未知项",
            "FACT_TARGET_BAND",
        ):
            self.assertIn(phrase, html)
            self.assertIn(phrase, markdown)
        self.assertIn("- 报告类型：决策型", markdown)
        self.assertIn("- 主任务：决策型及沃朗森30–50元牙膏定位", markdown)
        self.assertIn("- 子模块：洞察型供给结构；比较型前10竞品；评估型6张首屏图", markdown)
        self.assertIn("- 状态：绿色", markdown)
        self.assertIn("- 处理方式：自动生成", markdown)

    def test_renders_optional_deep_analysis_sections(self):
        profile = {
            "row_count": 80,
            "price_summary": {"median": 21.38},
            "sales_summary": {"median": 10000},
            "price_bands": [],
            "price_label_counts": [],
            "top_shops": [],
            "claim_counts": [],
        }
        facts = {
            "field_coverage": {},
            "ad_summary": {},
            "duplicate_summary": {},
            "title_phrases": [],
            "facts": [
                {
                    "id": "FACT_PRICE_LABELS",
                    "topic": "price_labels",
                    "denominator": 80,
                    "value": [],
                    "boundary": "空证据不应展示",
                }
            ],
            "deep_analysis": {
                "executive_snapshot": {
                    "strongest_conclusion": "目标价格带被单一品牌密集占位",
                    "biggest_limitation": "评价正文未取得",
                    "next_action": "先拆分 SKU，再做主图单变量测试",
                },
                "source_inventory": [
                    {
                        "name": "搜索商品样本",
                        "evidence_type": "结构化表格",
                        "scope": "80 个商品",
                        "source": "selection-live/market-sample.csv",
                        "usage": "价格、店铺、广告、标题和付款信号",
                    }
                ],
                "evidence_catalog": [
                    {
                        "id": "FACT_SAMPLE_SCOPE",
                        "display_name": "样本范围",
                        "evidence_type": "表格计算",
                        "source": "80 商品 CSV",
                        "summary": "80 个固定样本",
                        "boundary": "不外推全平台",
                    },
                    {
                        "id": "FACT_IMAGE_DIAGNOSIS",
                        "display_name": "首屏图片诊断",
                        "evidence_type": "图片证据",
                        "source": "6 张本地图片",
                        "summary": "逐张人工复核",
                        "boundary": "不推断点击率",
                    },
                ],
                "business_price_bands": [
                    {"band": "30–39.99", "rows": 10, "share": 0.125, "median_sales_signal": 20000}
                ],
                "ad_comparison": [
                    {"channel": "广告", "rows": 14, "median_price": 25, "median_sales_signal": 10000, "median_rank": 40}
                ],
                "claim_taxonomy": [
                    {"claim": "含氟防蛀", "rows": 31, "share": 0.3875, "role": "拥挤基础卖点"}
                ],
                "claim_cooccurrence": [
                    {"pair": "美白去黄 × 清新口气", "rows": 20, "share": 0.25}
                ],
                "brand_map": [
                    {"brand": "沃朗森", "rows": 14, "share": 0.175, "target_band_rows": 7, "median_price": 35}
                ],
                "wolongsen_skus": [
                    {"product_id": "1", "rank": 18, "price": 35, "sales_signal": 3000, "claims": "牙结石 / 美白"}
                ],
                "competitor_matrix": [
                    {"product_id": "1", "brand": "沃朗森", "archetype": "问题解决型", "search_price": 35, "live_price": 35, "price_delta": 0, "services": 4, "sku_groups": 1}
                ],
                "image_diagnostics": [
                    {
                        "asset_href": "evidence-images/wolongsen.webp",
                        "brand": "沃朗森",
                        "role": "功效主图",
                        "strength": "商品清晰",
                        "weakness": "信息过载",
                        "compliance_watch": "医用表达",
                    }
                ],
            },
        }

        html = MODULE.build_html(profile, "深度报告", facts, None)

        for phrase in (
            "核心结论",
            "最大限制",
            "下一步动作",
            "经营结构诊断",
            "卖点供给与共现",
            "品牌与店铺竞争",
            "前 10 竞品核验",
            "主图证据诊断",
            "目标价格带被单一品牌密集占位",
            "FACT_* 是机器证据编号，不是图片",
            "搜索商品样本",
            "evidence-images/wolongsen.webp",
        ):
            self.assertIn(phrase, html)
        self.assertNotIn("FACT_PRICE_LABELS", html)


if __name__ == "__main__":
    unittest.main()
