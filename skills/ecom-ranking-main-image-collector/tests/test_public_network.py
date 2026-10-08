import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('collector', Path(__file__).parents[1] / 'scripts/collect_main_images.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class PublicNetworkTests(unittest.TestCase):
    def test_rejects_private_reserved_and_credential_urls(self):
        for url in ('http://127.0.0.1/image', 'http://10.0.0.1/image', 'http://[::1]/image', 'https://user:placeholder@example.com/image'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.validate_public_http_url(url)

    def test_redirect_to_loopback_is_rejected(self):
        with self.assertRaises(ValueError):
            collector.PublicOnlyRedirectHandler().redirect_request(None, None, 302, '', {}, 'http://127.0.0.1/private')

    def test_explicit_loopback_origin_is_not_blanket_internal_access(self):
        origin='http://127.0.0.1:18086/command'
        self.assertEqual(collector.validate_public_http_url('http://127.0.0.1:18086/image', origin), 'http://127.0.0.1:18086/image')
        with self.assertRaises(ValueError):
            collector.validate_public_http_url('http://127.0.0.1:18087/image', origin)


if __name__ == '__main__':
    unittest.main()
