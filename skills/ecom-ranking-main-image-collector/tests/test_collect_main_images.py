import importlib.util
import json
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "collect_main_images.py"
SPEC = importlib.util.spec_from_file_location("collect_main_images", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StructuredInputTests(unittest.TestCase):
    def test_loads_products_from_kimi_webbridge_response_envelope(self):
        inner = {
            "url": "https://s.taobao.com/search?q=test&sort=sale-desc",
            "sort_selected": "销量",
            "products": [
                {
                    "rank": 1,
                    "item_id": "123456789012",
                    "item_url": "https://item.taobao.com/item.htm?id=123456789012",
                    "title": "儿童牙膏测试商品",
                    "image_url": "https://img.alicdn.com/test.jpg",
                    "price": "¥19.9",
                    "volume": "2万+人收货",
                }
            ],
        }
        envelope = {"ok": True, "data": {"type": "string", "value": json.dumps(inner, ensure_ascii=False)}}
        with tempfile.TemporaryDirectory() as root:
            source = Path(root) / "kimi-response.json"
            source.write_text(json.dumps(envelope, ensure_ascii=False), encoding="utf-8")
            records = MODULE.load_structured_products(source)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["item_id"], "123456789012")
        self.assertEqual(records[0]["rank"], "1")
        self.assertEqual(records[0]["source_url"], inner["url"])
        self.assertIn("Kimi WebBridge", records[0]["source_type"])
        self.assertEqual(records[0]["sort_selected"], "销量")

    def test_product_evidence_gate_rejects_logo_only_image(self):
        logo = {
            "image_url": "https://img.alicdn.com/taobao-logo.png",
            "product_name": "儿童牙膏 product 1",
        }
        product = {
            "image_url": "https://img.alicdn.com/item.jpg",
            "item_id": "123456789012",
            "item_url": "https://item.taobao.com/item.htm?id=123456789012",
            "title": "儿童牙膏真实商品",
        }
        self.assertFalse(MODULE.has_product_evidence(logo))
        self.assertTrue(MODULE.has_product_evidence(product))

    def test_cli_accepts_structured_json_as_a_collection_source(self):
        payload = {
            "url": "https://s.taobao.com/search?q=test&sort=sale-desc",
            "sort_selected": "销量",
            "products": [
                {
                    "rank": 1,
                    "item_id": "123456789012",
                    "item_url": "https://item.taobao.com/item.htm?id=123456789012",
                    "title": "儿童牙膏测试商品",
                    "image_url": "https://img.alicdn.com/test.jpg",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            source = root_path / "products.json"
            source.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--category",
                    "儿童牙膏",
                    "--platform",
                    "taobao",
                    "--structured-json",
                    str(source),
                    "--out",
                    str(root_path / "out"),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            manifests = list((root_path / "out").glob("*/manifest.csv"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(manifests), 1)

    def test_cli_marks_logo_only_html_as_insufficient_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            html_dir = root_path / "html"
            html_dir.mkdir()
            (html_dir / "search.html").write_text(
                '<a href="https://www.taobao.com"><img src="https://img.alicdn.com/taobao-brand.png"></a>',
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--category",
                    "儿童牙膏",
                    "--platform",
                    "taobao",
                    "--html-dir",
                    str(html_dir),
                    "--out",
                    str(root_path / "out"),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            manifest_path = next((root_path / "out").glob("*/manifest.csv"))
            with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(result.returncode, 1)
        self.assertEqual(rows[0]["status"], "insufficient_evidence")

    def test_enriched_sample_manifest_keeps_sort_and_price_labels(self):
        with tempfile.TemporaryDirectory() as root:
            out_dir = Path(root)
            outputs = out_dir / "outputs"
            outputs.mkdir()
            sample_path = outputs / "sample_manifest.csv"
            with sample_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["sample_id", "rank"])
                writer.writeheader()
                writer.writerow({"sample_id": "S001", "rank": "1"})
            MODULE.enrich_sample_manifest(out_dir, [{
                "rank": "1",
                "status": "downloaded",
                "sort_selected": "销量",
                "price_label": "优惠后",
                "raw_text": "2万+人收货",
            }])
            with sample_path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(rows[0]["sort_selected"], "销量")
        self.assertEqual(rows[0]["price_label"], "优惠后")
        self.assertEqual(rows[0]["raw_text"], "2万+人收货")


if __name__ == "__main__":
    unittest.main()
