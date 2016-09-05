class BotlangException(Exception):
    pass


class BotlangErrorException(Exception):

    def __init__(self, exception, execution_stack):

        super(BotlangErrorException, self).__init__(exception.message)
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
