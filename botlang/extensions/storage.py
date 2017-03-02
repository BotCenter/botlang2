class StorageApi(object):

    def put(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def get_or_else(self, key, else_function):
        raise NotImplementedError

    def remove(self, key):
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
