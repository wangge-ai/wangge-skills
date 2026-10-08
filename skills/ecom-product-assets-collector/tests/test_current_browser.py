import json
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "collect_product_assets.py"


def bmp_bytes(width: int, height: int) -> bytes:
    row_size = (width * 3 + 3) & ~3
    pixel_size = row_size * height
    header = b"BM" + struct.pack("<IHHI", 54 + pixel_size, 0, 0, 54)
    dib = struct.pack("<IIIHHIIIIII", 40, width, height, 1, 24, 0, pixel_size, 2835, 2835, 0, 0)
    row = bytes((160, 92, 45)) * width + b"\0" * (row_size - width * 3)
    return header + dib + row * height


class FakeWebBridgeHandler(BaseHTTPRequestHandler):
    actions = []
    image = bmp_bytes(300, 300)

    def log_message(self, *_args):
        return

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self.__class__.actions.append(payload["action"])
        if payload["action"] == "navigate":
            body = {"success": True, "url": payload["args"]["url"], "tabId": 7}
        elif payload["action"] == "evaluate":
            page = {
                "url": "https://detail.tmall.com/item.htm?id=927450710319",
                "title": "测试商品",
                "text": "商品详情",
                "blocked": False,
                "candidates": [{
                    "url": f"http://127.0.0.1:{self.server.server_port}/main.bmp",
                    "source": "dom-img",
                    "context": {
                        "chain": "SECTION.gallery.main-pic IMG",
                        "alt": "商品主图",
                        "top": 100,
                        "width": 300,
                        "height": 300,
                    },
                }],
            }
            body = {"type": "string", "value": json.dumps(page, ensure_ascii=False)}
        else:
            body = {"success": False}
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path != "/main.bmp":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/bmp")
        self.send_header("Content-Length", str(len(self.image)))
        self.end_headers()
        self.wfile.write(self.image)


class CurrentBrowserContractTests(unittest.TestCase):
    def setUp(self):
        FakeWebBridgeHandler.actions = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeWebBridgeHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def test_current_browser_route_reuses_webbridge_and_does_not_launch_playwright(self):
        with tempfile.TemporaryDirectory(prefix="product assets webbridge ") as raw:
            output = Path(raw) / "output"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--url",
                    "https://detail.tmall.com/item.htm?id=927450710319",
                    "--platform",
                    "tmall",
                    "--use-current-browser",
                    "--allow-local-assets",
                    "--webbridge-endpoint",
                    f"http://127.0.0.1:{self.server.server_port}/command",
                    "--scroll-rounds",
                    "0",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "completed")
            self.assertEqual(manifest["browser_route"], "current-browser-webbridge")
            self.assertEqual(manifest["download"], {"main": 1, "detail": 0, "skipped": 0})
            self.assertEqual(FakeWebBridgeHandler.actions, ["navigate", "evaluate"])
            self.assertNotIn("Playwright", result.stdout + result.stderr)
            self.assertIn("## 一句话结论", result.stdout)
            self.assertIn("## 关键结果", result.stdout)
            self.assertIn("## 主要产物", result.stdout)
            self.assertIn("## 下一步", result.stdout)

    def test_disconnected_current_browser_returns_not_available_without_fallback_window(self):
        with tempfile.TemporaryDirectory(prefix="product assets disconnected ") as raw:
            output = Path(raw) / "output"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--url",
                    "https://detail.tmall.com/item.htm?id=927450710319",
                    "--platform",
                    "tmall",
                    "--use-current-browser",
                    "--allow-local-assets",
                    "--webbridge-endpoint",
                    "http://127.0.0.1:1/command",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=8,
            )
            self.assertNotEqual(result.returncode, 0)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "not_available")
            self.assertEqual(manifest["browser_route"], "current-browser-webbridge")
            self.assertNotIn("Playwright", result.stdout + result.stderr)
            self.assertIn("## 一句话结论", result.stdout)
            self.assertIn("## 主要产物", result.stdout)


if __name__ == "__main__":
    unittest.main()
