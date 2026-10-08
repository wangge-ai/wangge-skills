import json
import importlib.util
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "collect_product_assets.py"


def load_collector_module():
    spec = importlib.util.spec_from_file_location("collect_product_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bmp_bytes(width: int, height: int, rgb=(72, 116, 184)) -> bytes:
    row_size = (width * 3 + 3) & ~3
    pixel_size = row_size * height
    header = b"BM" + struct.pack("<IHHI", 54 + pixel_size, 0, 0, 54)
    dib = struct.pack("<IIIHHIIIIII", 40, width, height, 1, 24, 0, pixel_size, 2835, 2835, 0, 0)
    b, g, r = rgb[2], rgb[1], rgb[0]
    row = bytes((b, g, r)) * width + b"\0" * (row_size - width * 3)
    return header + dib + row * height


class OfflineHtmlContractTests(unittest.TestCase):
    def test_http_fetch_route_is_unchanged_by_local_file_boundary(self):
        expected = b"remote-image-bytes"

        class Response:
            ok = True
            status = 200

            def body(self):
                return expected

        class Request:
            def __init__(self):
                self.calls = []

            def get(self, url, **kwargs):
                self.calls.append((url, kwargs))
                return Response()

        request = Request()
        module = load_collector_module()
        with patch.object(module.socket, "getaddrinfo", return_value=[(2, 1, 6, "", ("1.1.1.1", 443))]):
            actual = module.fetch_bytes(request, "https://example.com/product-image.jpg", Path("Z:/not-used"))
        self.assertEqual(actual, expected)
        self.assertEqual(request.calls[0][0], "https://example.com/product-image.jpg")

    def test_saved_html_with_spaced_path_is_deterministic_and_auditable(self):
        with tempfile.TemporaryDirectory(prefix="product assets ") as raw:
            root = Path(raw)
            saved = root / "saved page"
            saved.mkdir()
            main = bmp_bytes(300, 300, (45, 92, 160))
            (saved / "main hero.bmp").write_bytes(main)
            (saved / "main duplicate.bmp").write_bytes(main)
            (saved / "detail long.bmp").write_bytes(bmp_bytes(320, 620, (230, 160, 65)))
            (saved / "too small.bmp").write_bytes(bmp_bytes(50, 50, (120, 120, 120)))
            (saved / "brand logo.bmp").write_bytes(bmp_bytes(300, 300, (0, 0, 0)))
            html = saved / "商品 页面.html"
            html.write_text(
                """<!doctype html><html><body>
                <section class='gallery main-pic'>
                  <img src='main hero.bmp' alt='商品主图'>
                  <img src='main duplicate.bmp' alt='商品主图副本'>
                  <img src='too small.bmp' alt='商品主图小图'>
                </section>
                <section class='product-detail description'>
                  <img src='detail long.bmp' alt='商品详情图'>
                  <img src='missing detail.bmp' alt='商品详情缺失图'>
                </section>
                <aside class='brand-logo'><img src='brand logo.bmp' alt='品牌 logo'></aside>
                </body></html>""",
                encoding="utf-8",
            )
            output = root / "outputs" / "product assets"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--html-file", str(html), "--platform", "tmall",
                 "--headless", "--scroll-rounds", "0", "--output", str(output)],
                capture_output=True, text=True, encoding="utf-8", timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["download"], {"main": 1, "detail": 1, "skipped": 3})
            downloaded = [row for row in manifest["records"] if row["status"] == "downloaded"]
            self.assertEqual({row["group"] for row in downloaded}, {"main", "detail"})
            self.assertTrue(all(row["source_url"].startswith("file://") for row in manifest["records"]))
            self.assertTrue(all(len(row["sha256"]) == 64 for row in downloaded))
            self.assertEqual(len({row["sha256"] for row in downloaded}), 2)
            reasons = {row["reason"] for row in manifest["records"] if row["status"] != "downloaded"}
            self.assertIn("重复图片", reasons)
            self.assertIn("图片尺寸或文件大小不足", reasons)
            self.assertTrue(any(reason.startswith("下载失败：") for reason in reasons))
            files = sorted(str(path.relative_to(output)).replace("\\", "/") for path in output.rglob("*.*") if path.parent.name in {"main", "detail"})
            paths = sorted(row["local_path"].replace("\\", "/") for row in downloaded)
            self.assertEqual(files, paths)

    def test_saved_html_cannot_read_parent_cross_drive_or_unc_but_allows_chinese_child(self):
        with tempfile.TemporaryDirectory(prefix="product assets boundary ") as raw:
            root = Path(raw)
            saved = root / "保存 页面"
            child = saved / "中文 子目录"
            child.mkdir(parents=True)
            outside = root / "outside secret.bmp"
            outside_bytes = bmp_bytes(300, 300, (210, 35, 52))
            outside.write_bytes(outside_bytes)
            allowed = child / "中文 商品图.bmp"
            allowed.write_bytes(bmp_bytes(300, 300, (32, 146, 92)))
            html = saved / "商品 页面.html"
            html.write_text(
                """<!doctype html><html><body><section class='gallery main-pic'>
                <img src='../outside secret.bmp' alt='父目录外部图片'>
                <img src='file:///Z:/outside-drive-secret.bmp' alt='跨盘符外部图片'>
                <img src='file://invalid-server/share/outside-unc-secret.bmp' alt='UNC 外部图片'>
                <img src='中文 子目录/中文 商品图.bmp' alt='中文子目录商品主图'>
                </section></body></html>""",
                encoding="utf-8",
            )
            output = root / "output"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--html-file", str(html), "--platform", "tmall",
                 "--headless", "--scroll-rounds", "0", "--output", str(output)],
                capture_output=True, text=True, encoding="utf-8", timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["download"], {"main": 1, "detail": 0, "skipped": 3})
            downloaded = [row for row in manifest["records"] if row["status"] == "downloaded"]
            self.assertEqual(len(downloaded), 1)
            self.assertIn("%E4%B8%AD%E6%96%87", downloaded[0]["source_url"])
            self.assertNotEqual(downloaded[0]["sha256"], __import__("hashlib").sha256(outside_bytes).hexdigest())
            escaped = [row for row in manifest["records"] if row["status"] == "failed"]
            self.assertEqual(len(escaped), 3)
            self.assertTrue(all("本地资源越界" in row["reason"] for row in escaped))
            copied = [path.read_bytes() for path in (output / "main").glob("*")]
            self.assertNotIn(outside_bytes, copied)


if __name__ == "__main__":
    unittest.main()
