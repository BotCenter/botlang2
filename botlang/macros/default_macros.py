from botlang import Environment
from botlang.macros.macro_expander import MacroExpander


class DefaultMacros(object):

    DEFAULT_MACROS_SOURCE_ID = '<DEFAULT_MACROS>'

    @classmethod
    def get_macros_ast(cls):

        from botlang import Parser
        return Parser.parse("""
            (define-syntax-rule (defun name args body)
                (define name (function args body))
            )
    
            (define-syntax-rule (bot name args body)
                (define name (bot-node args body))
            )
        """, source_id='<DEFAULT_MACROS>', expand_macros=False)

    @classmethod
    def get_environment(cls):

        expander = MacroExpander()
        environment = Environment()

        for macro in cls.get_macros_ast():
            macro.accept(expander, environment)  # Populate environment

        return environment
