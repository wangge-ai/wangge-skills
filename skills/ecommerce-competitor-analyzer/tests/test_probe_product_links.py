import importlib.util
import socket
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "probe_product_links.py"
SPEC = importlib.util.spec_from_file_location("probe_product_links", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PublicUrlValidationTests(unittest.TestCase):
    def test_accepts_public_https_url(self):
        public_dns = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        with patch.object(MODULE.socket, "getaddrinfo", return_value=public_dns):
            self.assertEqual(
                MODULE.validate_public_http_url("https://item.example.com/product?id=123"),
                "https://item.example.com/product?id=123",
            )

    def test_rejects_non_http_and_embedded_credentials(self):
        credential_url = "https://" + "user:pass@" + "example.com/item"
        for value in ("file:///etc/passwd", "ftp://example.com/file", credential_url):
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE.validate_public_http_url(value)

    def test_rejects_local_and_private_targets(self):
        private_dns = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.168.1.10", 443))]
        with self.assertRaises(ValueError):
            MODULE.validate_public_http_url("http://127.0.0.1/admin")
        with self.assertRaises(ValueError):
            MODULE.validate_public_http_url("http://localhost/admin")
        with patch.object(MODULE.socket, "getaddrinfo", return_value=private_dns):
            with self.assertRaises(ValueError):
                MODULE.validate_public_http_url("https://internal.example/item")


if __name__ == "__main__":
    unittest.main()
