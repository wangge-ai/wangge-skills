import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "analyze_competitors.py"
SPEC = importlib.util.spec_from_file_location("analyze_competitors", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompetitorEvidenceReportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            MODULE.canonicalize_row({
                "sample_id": "S001", "rank": "1", "platform": "淘宝",
                "product_name": "广告商品", "price": "¥71", "price_label": "首单价",
                "volume": "本月行业热销", "is_ad": "yes", "sort_selected": "销量",
                "source_type": "Kimi logged-in sales-sorted search DOM; page-order sample",
                "item_url": "https://item.taobao.com/item.htm?id=1",
            }),
            MODULE.canonicalize_row({
                "sample_id": "S002", "rank": "2", "platform": "淘宝",
                "product_name": "自然商品", "price": "¥16.9", "price_label": "补贴后",
                "volume": "3万+人收货", "is_ad": "no", "sort_selected": "销量",
                "source_type": "Kimi logged-in sales-sorted search DOM; page-order sample",
                "item_url": "https://detail.tmall.com/item.htm?id=2",
            }),
        ]

    def test_report_exposes_denominator_ads_price_and_sales_scope(self):
        report = MODULE.build_report(self.rows, "儿童牙膏")
        self.assertIn("总样本 2 条；自然样本 1 条；广告样本 1 条", report)
        self.assertIn("首单价", report)
        self.assertIn("补贴后", report)
        self.assertIn("3万+人收货", report)
        self.assertIn("页面展示信号，不等于真实成交量", report)
        self.assertIn("[S001]", report)
        self.assertIn("页面顺序不等于官方榜单名次", report)
        self.assertIn("价格口径分布", report)
        self.assertIn("| 补贴后 | 1 | 16.90 | 16.90 |", report)
        self.assertIn("广告样本不进入自然样本价格区间", report)

    def test_structured_facts_keep_provenance_and_unknowns(self):
        facts = MODULE.build_facts(self.rows, "儿童牙膏")
        self.assertEqual(facts["denominator"], {"total": 2, "organic": 1, "ads": 1})
        self.assertEqual(facts["items"][0]["price_scope"], "首单价")
        self.assertEqual(facts["items"][1]["sales_display"], "3万+人收货")
        self.assertEqual(facts["items"][0]["evidence_id"], "S001")
        self.assertIn("reviews", facts["missing_fields"])
        self.assertFalse(facts["allowed_inference"]["market_share"])


if __name__ == "__main__":
    unittest.main()
