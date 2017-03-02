import unittest

from botlang import BotlangSystem
from botlang.extensions.cache import CacheApi
from botlang.extensions.storage import StorageApi


class DummyDB(StorageApi):

    def __init__(self):
        self.backend = {}

    def put(self, key, value):
        self.backend[key] = value

    def get(self, key):
        return self.backend.get(key)

    def get_or_else(self, key, else_function):
        element = self.get(key)
        if element is None:
            self.put(key, else_function())
            return self.get(key)
        else:
            return element

    def remove(self, key):
        del self.backend[key]


class StorageExtensionTestCase(unittest.TestCase):

    def test_local_storage(self):

        db = DummyDB()
        runtime = BotlangSystem.bot_instance().setup_local_storage(db)
        results = runtime.eval("""
        (localdb-put "test1" 444)
        (localdb-put "test2" "miau")
        [define got1 (localdb-get-or-else "test3" (function () ":3"))]
        [define got2 (localdb-get-or-else "test3" (function () "3:"))]
        (localdb-remove "test2")
        (make-dict
            (list
                (list "test1" (localdb-get "test1"))
                (list "test2" (localdb-get "test2"))
                (list "got1" got1)
                (list "got2" got2)
            )
        )
        """)
        self.assertEqual(results['test1'], 444)
        self.assertEqual(results['test2'], None)
        self.assertEqual(results['got1'], ':3')
        self.assertEqual(results['got2'], ':3')

    def test_global_storage(self):

        db = DummyDB()
        runtime = BotlangSystem.bot_instance().setup_global_storage(db)
        results = runtime.eval("""
        (globaldb-put "test1" 444)
        (globaldb-put "test2" "miau")
        [define got1 (globaldb-get-or-else "test3" (function () ":3"))]
        [define got2 (globaldb-get-or-else "test3" (function () "3:"))]
        (globaldb-remove "test2")
        (make-dict
            (list
                (list "test1" (globaldb-get "test1"))
                (list "test2" (globaldb-get "test2"))
                (list "got1" got1)
                (list "got2" got2)
            )
        )
        """)
        self.assertEqual(results['test1'], 444)
        self.assertEqual(results['test2'], None)
        self.assertEqual(results['got1'], ':3')
        self.assertEqual(results['got2'], ':3')