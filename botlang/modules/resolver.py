class DuplicateModuleException(Exception):

    def __init__(self, module_name):
        super(DuplicateModuleException, self).__init__(
            'A module of name "{0}" is already defined'.format(module_name)
        )


class ModuleNotFoundException(Exception):

    def __init__(self, module_name):
        super(ModuleNotFoundException, self).__init__(
            'Module named "{0}" not found'.format(module_name)
        )


class ModuleResolver(object):

    def __init__(self):

        self.modules = {}

    def add_module(self, module):

        if self.modules.get(module.name) is not None:
            raise DuplicateModuleException(module.name)
        self.modules[module.name] = module

    def get_bindings(self, module_name):

        module = self.modules.get(module_name)
        if module is None:
            raise ModuleNotFoundException(module_name)
        return module.get_bindings(self)

    def load_modules(self, paths):

        from botlang import BotlangSystem

        for path in paths:
            module_file = open(path, 'r')
            module_str = module_file.read()
            module_file.close()
            BotlangSystem.run(
                module_str,
                module_resolver=self,
                source_id=path
            )
