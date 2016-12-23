class CacheApi(object):

    def put(self, key, value, expiration=None):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def get_or_else(self, key, else_function, expiration=None):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError


class CacheExtension(object):

    @classmethod
    def enable_cache(cls, botlang_system, cache_implementation):

        botlang_system.environment.add_cachable_primitives({
            'cache-put': cache_implementation.put,
            'cache-get': cache_implementation.get,
            'cache-get-or-else': cache_implementation.get_or_else,
            'cache-remove': cache_implementation.remove
        })
        return botlang_system
