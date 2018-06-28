
'''
===============================
Unit tests for module decorator
===============================

Unit tests for decorator
'''
from functools import wraps
import unittest
from drytools.decorator import decorator_factory, args2attrs
from drytools.annotation.composition import compose_annotations
from drytools.annotation.functions import iterify

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


class Test_args2attrs(unittest.TestCase):
    @compose_annotations
    def assertOrdinaryAttrs(self, inst, expected_attrs:(iterify, set)):
        actual_attrs = {a for a in dir(inst) if not a.startswith('_')}
        self.assertEqual(actual_attrs, expected_attrs)
    def test_restrict_to_1(self):
        class has_b:
            @args2attrs(restrict_to='b')
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(has_b(1, 2, v=3, w=4), 'b')
    def test_restrict_to_2(self):
        class has_b_v:
            @args2attrs(restrict_to=('b', 'v'))
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(has_b_v(5, 6, v=7, w=8), ('b', 'v'))
    def test_kw_default(self):
        restrict_to = ('v', 'args')
        class cls:
            @args2attrs(restrict_to=restrict_to)
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(cls(9, 10, w=11), restrict_to)
    def test_exclude(self):
        exclude = {'v', 'args'}
        class cls:
            @args2attrs(exclude=exclude)
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(cls(12, 13, w=14), ['a', 'b', 'u', 'w'])
    def test_empty_varargs(self):
        class cls:
            @args2attrs
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(cls(14, 15, w=16), ['a', 'b', 'args', 'u', 'v', 'w'])
    def test_empty_varkw(self):
        class cls:
            @args2attrs(expand_kw=False)
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(cls(17, 18), ['a', 'b', 'args', 'u', 'v', 'kwargs'])
    def test_expand_kw(self):
        exclude = {'v', 'args'}
        class cls:
            @args2attrs(exclude=exclude, expand_kw=False)
            def __init__(self, a, b, *args, u=None, v=1, **kwargs):
                pass
        self.assertOrdinaryAttrs(cls(19, 20, w=21), ['a', 'b', 'u', 'kwargs'])



if __name__ == '__main__':
    unittest.main()
