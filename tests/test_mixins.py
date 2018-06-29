
'''
============================
Unit tests for module mixins
============================

Unit tests for mixins
'''
import unittest

from drytools.mixins import repr_from_init
from drytools.decorator import args2attrs

class Test_repr_from_init(unittest.TestCase):
    def test_positional(self):
        class tst(repr_from_init):
            @args2attrs
            def __init__(self, a, b, c):
                pass
        self.assertEqual(repr(tst(1, True, 'foo')), "tst(1, True, 'foo')")
    def test_var_positional(self):
        class tst(repr_from_init):
            @args2attrs
            def __init__(self, *args):
                pass
        self.assertEqual(repr(tst(1, True, 'foo')), "tst(1, True, 'foo')")
    def test_kw(self):
        class tst(repr_from_init):
            @args2attrs
            def __init__(self, a=1, b=True, c='foo'):
                pass
        self.assertEqual(repr(tst(1, False, 'foo')), "tst(b=False)")
    def test_var_kw(self):
        class tst(repr_from_init):
            @args2attrs(expand_kw=False)
            def __init__(self, **kwargs):
                pass
        self.assertEqual(repr(tst(b=True, a=1, c='foo')), "tst(a=1, b=True, c='foo')")
    def test_all_ex_var_kw(self):
        class tst(repr_from_init):
            @args2attrs
            def __init__(self, a, b, *args, c='foo', d='bar'):
                pass
        self.assertEqual(repr(tst(1, 2, 3, 4, 5, c='foo', d='not bar')), "tst(1, 2, 3, 4, 5, d='not bar')")
    def test_all_inc_var_kw(self):
        class tst(repr_from_init):
            @args2attrs(expand_kw=False)
            def __init__(self, a, b, *args, c='foo', d='bar', **kwargs):
                pass
        self.assertEqual(repr(tst(1, 2, 3, 4, 5, c='foo', d='not bar', y='aa', x=3.14, q=1)), "tst(1, 2, 3, 4, 5, d='not bar', q=1, x=3.14, y='aa')")
    def test_raisesAttributeError(self):
        class tst(repr_from_init):
            def __init__(self, a):
                pass
        with self.assertRaises(AttributeError):
            repr(tst(1))



if __name__ == '__main__':
    unittest.main()
