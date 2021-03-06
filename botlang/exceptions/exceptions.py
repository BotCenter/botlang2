class BotlangException(Exception):

    def __init__(self, message):
        self.message = message


class BotlangErrorException(BotlangException):

    def __init__(self, exception, execution_stack):

        super(BotlangErrorException, self).__init__(exception.args[0])
        self.wrapped = exception
        self.stack = execution_stack

    def print_stack_trace(self):

        return 'Stack trace:\n{0}\n{1}:\n{2}'.format(
            self.stack.print_trace(),
            type(self.wrapped).__name__,
            self.message
        )

    def __str__(self):
        if isinstance(self.message, str):
            return self.message
        else:
            return self.message.__str__()


class BotlangAssertionException(BotlangException):
    pass
