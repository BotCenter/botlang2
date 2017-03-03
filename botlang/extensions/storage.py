class StorageApi(object):

    def put(self, key, value, expiration=None):
        """
        Set a key->value association in the store with an expiration flag of
        <expiration> milliseconds.

        :param key: string
        :param value: any
        :param expiration: milliseconds or None for unbounded persistence
        """
        raise NotImplementedError

    def get(self, key):
        """
        Try to retrieve <key>'s associated value from the store. Returns None
        if no value is found.

        :param key: string
        """
        raise NotImplementedError

    def get_or_else(self, key, else_function, expiration=None):
        """
        Try to retrieve <key>'s associated value from the store. If the value
        does not exist, it is computed by applying <else_function> and then
        added to the store with an expiration of <expiration> milliseconds.

        :param key: string
        :param else_function: a function which does not take parameters
        :param expiration: milliseconds or None for unbounded persistence
        """
        raise NotImplementedError

    def remove(self, key):
        """
        Removes a key->value association from the store

        :param key: string
        """
        raise NotImplementedError


class LocalStorageExtension(object):

    @classmethod
    def apply(cls, botlang_system, db_implementation):

        botlang_system.environment.add_primitives({
            'localdb-put': db_implementation.put,
            'localdb-get': db_implementation.get,
            'localdb-get-or-else': db_implementation.get_or_else,
            'localdb-remove': db_implementation.remove
        })
        return botlang_system


class GlobalStorageExtension(object):

    @classmethod
    def apply(cls, botlang_system, db_implementation):

        botlang_system.environment.add_primitives({
            'globaldb-put': db_implementation.put,
            'globaldb-get': db_implementation.get,
            'globaldb-get-or-else': db_implementation.get_or_else,
            'globaldb-remove': db_implementation.remove
        })
        return botlang_system


class CacheExtension(object):

    @classmethod
    def apply(cls, botlang_system, cache_implementation):

        botlang_system.environment.add_primitives({
            'cache-put': cache_implementation.put,
            'cache-get': cache_implementation.get,
            'cache-get-or-else': cache_implementation.get_or_else,
            'cache-remove': cache_implementation.remove
        })
        return botlang_system
