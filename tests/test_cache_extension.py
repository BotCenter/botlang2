import unittest

from botlang import BotlangSystem
from botlang.extensions.cache import CacheApi


class DummyCache(CacheApi):
    def __init__(self):
        self.backend = {}

    def put(self, key, value, expiration=None):
        self.backend[key] = value

    def get(self, key):
        return self.backend.get(key)

    def get_or_else(self, key, else_function, expiration=None):
        element = self.get(key)
        if element is None:
            self.put(key, else_function(), expiration)
            return self.get(key)
        else:
            return element

    def remove(self, key):
        del self.backend[key]


class CacheExtensionTestCase(unittest.TestCase):

    def test_cache(self):

        cache = DummyCache()
        runtime = BotlangSystem.bot_instance().setup_cache_extension(cache)
        results = runtime.eval("""
        (cache-put "test1" 444)
        (cache-put "test2" "miau")
        [define got1 (cache-get-or-else "test3" (function () ":3"))]
        [define got2 (cache-get-or-else "test3" (function () "3:"))]
        (cache-remove "test2")
        (make-dict
            (list
                (list "test1" (cache-get "test1"))
                (list "test2" (cache-get "test2"))
                (list "got1" got1)
                (list "got2" got2)
            )
        )
        """)
        self.assertEqual(results['test1'], 444)
        self.assertEqual(results['test2'], None)
        self.assertEqual(results['got1'], ':3')
        self.assertEqual(results['got2'], ':3')
