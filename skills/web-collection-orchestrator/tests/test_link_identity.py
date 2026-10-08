import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('queue', Path(__file__).parents[1] / 'scripts/normalize_link_queue.py')
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)


class LinkIdentityTests(unittest.TestCase):
    def test_different_articles_and_products_are_not_merged(self):
        for left, right in [
            ('https://mp.weixin.qq.com/s?__biz=demo&mid=1&idx=1&sn=a', 'https://mp.weixin.qq.com/s?__biz=demo&mid=2&idx=1&sn=b'),
            ('https://item.taobao.com/item.htm?id=101', 'https://item.taobao.com/item.htm?id=102'),
            ('https://mp.weixin.qq.com/s/AbCd', 'https://mp.weixin.qq.com/s/abcd'),
        ]:
            self.assertNotEqual(queue.canonicalize(left)[1], queue.canonicalize(right)[1])

    def test_tracking_duplicates_remove_credentials(self):
        left, key = queue.canonicalize('https://example.com/item?id=101&utm_source=demo&token=private-example#top')
        right, other = queue.canonicalize('https://example.com/item?utm_source=other&id=101')
        self.assertEqual(key, other)
        self.assertEqual(left, right)
        self.assertNotIn('private-example', left)


if __name__ == '__main__':
    unittest.main()
