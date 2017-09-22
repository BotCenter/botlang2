from botlang import Environment, Parser
from botlang.macros.macro_expander import MacroExpander


class DefaultMacros(object):

    MACROS = Parser.parse("""
        (define-syntax-rule (defun name args body)
            (define name (function args body))
        )

        (define-syntax-rule (bot name args body)
            (define name (bot-node args body))
        )
    """, source_id='<default macros>')

    @classmethod
    def get_environment(cls):

        expander = MacroExpander()
        environment = Environment()

        for macro in cls.MACROS:
            macro.accept(expander, environment)  # Populate environment

        return environment
