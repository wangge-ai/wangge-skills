import argparse
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_main_image_report.py"
SPEC = importlib.util.spec_from_file_location("build_main_image_report", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReportContractTests(unittest.TestCase):
    def test_report_exposes_collection_facts_and_operational_boundary(self):
        rows = [
            {
                "rank": "1",
                "platform": "淘宝",
                "title": "广告样本",
                "item_id": "111111111111",
                "image_url": "https://img.alicdn.com/ad.jpg",
                "is_ad": "yes",
                "sort_selected": "销量",
                "price_label": "补贴后",
            },
            {
                "rank": "2",
                "platform": "淘宝",
                "title": "自然位样本",
                "item_id": "222222222222",
                "image_url": "https://img.alicdn.com/organic.jpg",
                "is_ad": "no",
                "sort_selected": "销量",
                "price_label": "优惠后",
            },
        ]
        with tempfile.TemporaryDirectory() as root:
            args = argparse.Namespace(
                out=str(Path(root) / "report.html"),
                asset_root=root,
                manifest=str(Path(root) / "manifest.csv"),
                category="儿童牙膏",
                per_platform=20,
                max_cards=20,
                max_table_rows=20,
                title="儿童牙膏销量排序主图样本报告",
                source_note="销量排序搜索页顺序样本；不等同于官方榜单。",
                readme_note="广告位单列。",
                contact_sheet="",
            )
            page = MODULE.build_html(args, rows)

        self.assertIn("10 秒事实层", page)
        self.assertIn("自然位样本", page)
        self.assertIn("广告位样本", page)
        self.assertIn("运营使用层", page)
        self.assertIn("不等同于官方榜单", page)
        self.assertIn("当前样本来自 销量排序搜索页", page)
        self.assertIn("overflow-wrap: anywhere", page)
        self.assertIn("min-width: 0", page)
        self.assertIn("max-width: 100%", page)
        self.assertIn("word-break: break-all", page)


if __name__ == "__main__":
    unittest.main()
