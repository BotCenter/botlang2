from botlang.evaluation.values import NativeException


def is_exception(value):
    return isinstance(value, NativeException)


def try_catch_complete(process, failure,
                       after_execution=lambda: None, prod=True):
    exception = None
    try:
        value = process()
        if is_exception(value):
            exception = value
            raise Exception()
    except Exception as python_exception:
        if exception is None:
            if prod:
                exception = NativeException('system', 'system')
            else:
                exception = NativeException('system',
                                            r"""Exception:
                                            {}""".format(python_exception))
        failure(exception)
    finally:
        after_execution()


def public_try_catch(process, failure, after_execution=lambda: None):
    try_catch_complete(process, failure, after_execution, True)


def develop_try_catch(process, failure, after_execution=lambda: None):
    try_catch_complete(process, failure, after_execution, False)


EXCEPTION_PRIMITIVES = {
    'exception?': is_exception,
    'try-catch': public_try_catch,
    'try-catch-verbose': develop_try_catch
}
