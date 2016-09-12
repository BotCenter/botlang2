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


class BotlangTester(object):

    @classmethod
    def get_send_message(cls, mocks):

        if mocks is None:
            mocks = {}

        def send_message(bot, message):
            bot_code, evaluation_state = bot
            system = BotlangSystem.bot_instance()
            system.environment.update(mocks)
            result = system.eval_bot(
                bot_code,
                message,
                evaluation_state
            )
            return {
                'bot': (bot_code, result.execution_state),
                'message': result.message,
                'data': result.data
            }

        return send_message

    @classmethod
    def botlang_test_instance(cls, mocks=None):

        environment = BotlangSystem.base_environment()
        environment.add_primitives({
            'assert': assert_function,
            'assert-equal?': assert_equals_function,
            'send-message': cls.get_send_message(mocks)
        })

        return BotlangSystem(environment.new_environment())

    @classmethod
    def get_mocks(cls, tests_code):

        mock_system = BotlangSystem()
        mock_system.eval(tests_code)
        mock_bindings = {
            name[5:]: value
            for name, value in mock_system.environment.bindings.items()
            if name.startswith('mock-')
        }
        return mock_bindings

    @classmethod
    def post_setup_test_instance(cls, tests_code, bot_code):

        mock_bindings = cls.get_mocks(tests_code)
        setup_system = cls.botlang_test_instance(mock_bindings)
        setup_system.eval(tests_code)

        setup_bindings = {
            name[6:]: function.apply((bot_code, ExecutionState([], 0)))
            for name, function in setup_system.environment.bindings.items()
            if name.startswith('setup-')
        }

        setup_system.environment.update(setup_bindings)
        return setup_system

    @classmethod
    def run(cls, bot_code, tests_code):

        test_system = cls.post_setup_test_instance(tests_code, bot_code)

        test_functions = {
            name: function for name, function
            in test_system.environment.bindings.items()
            if name.startswith('test-')
        }

        results = []
        for test_name, test_function in test_functions.items():
            try:
                test_function.apply(
                    (bot_code, ExecutionState([], 0))
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

    def to_dict(self):
        raise NotImplementedError


class SuccessfulTestResult(TestResult):

    def __init__(self, name):
        super(SuccessfulTestResult, self).__init__(name)

    def is_success(self):
        return True

    def to_dict(self):
        return {
            'test_name': self.name,
            'result': 'passed'
        }


class FailedTestResult(TestResult):

    def __init__(self, name, failure):
        super(FailedTestResult, self).__init__(name)
        self.failed_assert = failure

    def is_failure(self):
        return True

    def to_dict(self):
        return {
            'test_name': self.name,
            'result': 'failed',
            'message': self.failed_assert.message
        }


class ErrorTestResult(TestResult):

    def __init__(self, name, error):
        super(ErrorTestResult, self).__init__(name)
        self.error = error

    def is_error(self):
        return True

    def to_dict(self):
        return {
            'test_name': self.name,
            'result': 'error',
            'message': self.error.message
        }
