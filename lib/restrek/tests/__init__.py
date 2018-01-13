import re
from restrek.core.display import display
import test_lib.common


def assert_eq(expected, actual, msg=None):
    r = (expected == actual)
    failed_reason = None
    if not r:
        failed_reason = 'Expected `%s` but got `%s`' % (expected, actual)
    return r, msg, failed_reason


def assert_ex(val, msg=None):
    r = (val is not None)
    failed_reason = None
    if not r:
        failed_reason = 'Value `%s` is unkown' % val
    return r, msg, failed_reason


def assert_regex(val, regex='', msg=None):
    _regex = re.compile(regex, re.I)
    match = _regex.match(val)
    r = bool(match)
    failed_reason = None
    if not r:
        failed_reason = 'Value `%s` does not match pattern `%s`' % (val, regex)
    return r, msg, failed_reason


class TestError(Exception):

    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return 'Error: %s' % self.message

    def __repr__(self):
        return self.message


class TestsManager(object):

    def __init__(self):
        pass

    def _build_context(self, output):
        ctx = dict(assert_eq=assert_eq,
                   assert_ex=assert_ex,
                   assert_regex=assert_regex)
        ctx.update(output)
        return ctx

    def assert_tests(self, test_statements=[], output=dict()):
        ctx = self._build_context(output)
        for test_stmt in test_statements:
            yield self._run_test(test_stmt, ctx)

    def _run_test(self, test, ctx):
        results = False
        try:
            results, msg, failed_reason = eval(test, {}, ctx)
            if msg is None:
                msg = test
            if results:
                display.success('[Assert] %s : %s' % (msg, 'OK'))
            else:
                display.err('[Assert] %s : %s, %s' % (msg, 'FAILED', failed_reason))
                display.err('-------\n%r\n-------\n' % ctx)
        except (NameError, KeyError, TypeError, SyntaxError, IndexError) as e:
            display.err('Error: %s - %s' % (test, e))
            display.err('%r' % ctx)

        return results
