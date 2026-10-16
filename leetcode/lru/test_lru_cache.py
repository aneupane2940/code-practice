"""Behavior checks, including a deterministic reference-model comparison."""
from collections import OrderedDict
import random
import sys
import unittest

if "--practice" in sys.argv:
    sys.argv.remove("--practice")
    from practice import LRUCache
else:
    from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_example(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        cache.put(3, 30)
        self.assertEqual(cache.get(2), -1)
        cache.put(4, 40)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 30)
        self.assertEqual(cache.get(4), 40)

    def test_update_refreshes_recency(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(1, 99)
        cache.put(3, 30)
        self.assertEqual(cache.get(2), -1)
        self.assertEqual(cache.get(1), 99)

    def test_miss_does_not_change_recency(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(999), -1)
        cache.put(3, 30)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 10)
        cache.put(1, 11)
        self.assertEqual(cache.get(1), 11)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)

    def test_zero_capacity(self):
        cache = LRUCache(0)
        cache.put(1, 10)
        self.assertEqual(cache.get(1), -1)

    def test_negative_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(-1)

    def test_reference_model(self):
        rng = random.Random(42)
        for capacity in range(5):
            cache = LRUCache(capacity)
            reference = OrderedDict()
            for _ in range(500):
                key = rng.randrange(8)
                if rng.randrange(2):
                    value = rng.randrange(100)
                    cache.put(key, value)
                    if capacity:
                        reference[key] = value
                        reference.move_to_end(key)
                        if len(reference) > capacity:
                            reference.popitem(last=False)
                else:
                    expected = reference.get(key, -1)
                    if key in reference:
                        reference.move_to_end(key)
                    self.assertEqual(cache.get(key), expected)
            # Check remaining contents, including all keys that were evicted.
            for key in range(8):
                self.assertEqual(cache.get(key), reference.get(key, -1))


if __name__ == "__main__":
    unittest.main()
