from unittest import TestCase
from lru_cache import LRUCache


class TestLRUCache(TestCase):
    def test_set_and_get(self):
        cache = LRUCache()
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)

    def test_get_unknown_key(self):
        cache = LRUCache()
        with self.assertRaises(KeyError):
            cache.get("a")

    def test_invalid_limit(self):
        with self.assertRaises(TypeError):
            LRUCache(True)

        with self.assertRaises(TypeError):
            LRUCache('abc')

        with self.assertRaises(ValueError):
            LRUCache(0)

        with self.assertRaises(ValueError):
            LRUCache(-1)

        LRUCache(40)

    def test_overcome_limit(self):
        cache = LRUCache(2)
        cache['a'] = 1
        cache['b'] = 2
        cache['c'] = 3

        with self.assertRaises(KeyError):
            print(cache['a'])

        self.assertEqual(cache['b'], 2)
        self.assertEqual(cache['c'], 3)

    def test_order_changed(self):
        cache = LRUCache(2)
        cache['a'] = 1
        cache['b'] = 2
        # проверим, что при обращении изменяется порядок
        _ = cache['a']
        cache['c'] = 3

        with self.assertRaises(KeyError):
            print(cache['b'])

        cache = LRUCache(2)
        cache['a'] = 1
        cache['b'] = 2
        # проверим, что при изменении значения порядок тоже изменяется
        cache['a'] = 4
        cache['c'] = 3

        with self.assertRaises(KeyError):
            print(cache['b'])
