class BotlangException(Exception):

    def __init__(self, message):
        self.message = message


class BotlangErrorException(BotlangException):

    def __init__(self, exception, execution_stack):

        # Disgusting trick for compatibility with Python 2 and 3
        try:
            message = exception.args[0]
        except IndexError:
            message = exception.message

        super(BotlangErrorException, self).__init__(message)
        self.wrapped = exception
        self.stack = execution_stack

    def print_stack_trace(self):

        return '\nStack trace:\n{0}\n\n{1}:\n{2}'.format(
            self.stack.print_trace(),
            type(self.wrapped).__name__,
            self.message
        )


class BotlangAssertionException(BotlangException):
    pass
