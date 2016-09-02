from botlang import BotlangSystem
from botlang.evaluation.evaluator import ExecutionState
from botlang.exceptions.exceptions import *


def assert_function(expression):

    if not expression:
        raise BotlangAssertionException('Expression evaluated to false')


def assert_equals_function(expression, expected):

    if expression != expected:
        raise BotlangAssertionException(
            '{0} != {1}'.format(expression, expected)
        )


def send_message(bot, message):

    bot_code, evaluation_state = bot
    result = BotlangSystem.bot_instance().eval_bot(
        bot_code,
        message,
        evaluation_state
    )
    return {
        'bot': (bot_code, result.execution_state),
        'message': result.message,
        'data': result.data
    }


class BotlangTester(object):

    def __init__(self, bot_code, tests_code):

        self.bot_code = bot_code
        self.tests_code = tests_code

    @classmethod
    def botlang_test_instance(cls, additional_bindings=None):

        environment = BotlangSystem.base_environment()
        environment.add_primitives({
            'assert': assert_function,
            'assert-equal?': assert_equals_function,
            'send-message': send_message
        })

        if additional_bindings is None:
            additional_bindings = {}

        return BotlangSystem(environment.new_environment(additional_bindings))

    def post_setup_test_instance(self):

        setup_system = self.botlang_test_instance()
        setup_system.eval(self.tests_code)

        setup_bindings = {
            name[6:]: function.apply((self.bot_code, ExecutionState([], 0)))
            for name, function in setup_system.environment.bindings.items()
            if name.startswith('setup-')
        }

        setup_system.environment.update(setup_bindings)
        return setup_system

    def run(self):

        test_system = self.post_setup_test_instance()

        test_functions = {
            name: function for name, function
            in test_system.environment.bindings.items()
            if name.startswith('test-')
        }

        results = []
        for test_name, test_function in test_functions.items():
            try:
                test_function.apply(
                    (self.bot_code, ExecutionState([], 0))
                )
                results.append(SuccessfulTestResult(test_name))

            except BotlangAssertionException as assertion:
                results.append(FailedTestResult(test_name, assertion))

            except BotlangErrorException as error:
                results.append(ErrorTestResult(test_name, error))

        return results


class TestResult(object):

    def __init__(self, test_name):
        self.name = test_name

    def is_success(self):
        return False

    def is_failure(self):
        return False

    def is_error(self):
        return False


class SuccessfulTestResult(TestResult):

    def __init__(self, name):
        super(SuccessfulTestResult, self).__init__(name)

    def is_success(self):
        return True


class FailedTestResult(TestResult):

    def __init__(self, name, failure):
        super(FailedTestResult, self).__init__(name)
        self.failed_assert = failure

    def is_failure(self):
        return True


class ErrorTestResult(TestResult):

    def __init__(self, name, error):
        super(ErrorTestResult, self).__init__(name)
        self.error = error

    def is_error(self):
        return True
