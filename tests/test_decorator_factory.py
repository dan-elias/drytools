
'''
=======================================
Unit tests for module decorator_factory
=======================================

Unit tests for decorator_factory
'''

from functools import wraps
import unittest
from drytools.decorator_factory import decorator_factory

class Test_decorator_factory(unittest.TestCase):
    def setUp(self):
        @decorator_factory
        def decorator_and_func_args(da='a', db='b'):
            decorator_kwarg_items = sorted(locals().items())
            def decorator(fun):
                @wraps(fun)
                def wrapped(*args, **kwargs):
                    fun(*args, **kwargs)
                    return (decorator_kwarg_items, args, sorted(kwargs.items()))
                return wrapped
            return decorator
        @decorator_and_func_args
        def decorated_with_no_parentheses(p1, p2, k1=1, k2=2):
            pass
        @decorator_and_func_args()
        def decorated_with_empty_parentheses(p1, p2, k1=1, k2=2):
            pass
        @decorator_and_func_args(db='bb', da='aa')
        def decorated_with_args(p1, p2, k1=1, k2=2):
            pass
        _locals = locals()
        self.test_funcs = {k: v for k, v in _locals.items() if k.startswith('decorated_with')}
    def test_retval_equal(self):
        for decorated_with, args, kwargs, retval in [
                ('no_parentheses', (1,2), {}, ([('da', 'a'), ('db', 'b')], (1,2), [])),
                ('empty_parentheses', (1,2), {}, ([('da', 'a'), ('db', 'b')], (1,2), [])),
                ('args', (1,2), {}, ([('da', 'aa'), ('db', 'bb')], (1,2), [])),
                ]:
            test_func = self.test_funcs['decorated_with_{decorated_with}'.format(**locals())]
            for v1, v2 in zip(test_func(*args, **kwargs), retval):
                self.assertEqual(v1, v2)
    def test_TypeError(self):
        for decorated_with, args, kwargs in [
                ('no_parentheses', (1,), {}),
                ('empty_parentheses', (1,), {}),
                ('args', (1,), {}),
                ]:
            test_func = self.test_funcs['decorated_with_{decorated_with}'.format(**locals())]
            with self.assertRaises(TypeError):
                test_func(*args, **kwargs)

if __name__ == '__main__':
    unittest.main()


