
'''
==========================================
Unit tests for module annotation.functions
==========================================

Unit tests for annotation.functions
'''
from collections import OrderedDict
from collections.abc import Iterator
from itertools import count
from operator import gt
import unittest
from drytools.annotation.functions import check, iterify

class Test_check(unittest.TestCase):
    def setUp(self):
        self.got_3_args = lambda *args, **kwargs: (len(args) + len(kwargs)) == 3
    def test_retval_equal(self):
        for calc, retval in [(lambda: check(gt, 2)(3), 3),
                             (lambda: check(self.got_3_args, 1, 2)(5), 5),
                             (lambda: check(self.got_3_args, 1, a='a')(6), 6),
                             (lambda: check(self.got_3_args, p=1, q=2)(7), 7),
                            ]:
            self.assertEqual(calc(), retval)
    def test_raises(self):
        for calc, errtype in [(lambda: check(gt, 2)(1), ValueError),
                              (lambda: check(self.got_3_args, 1, 2, 3, raises=TypeError)(5), TypeError),
                              (lambda: check(self.got_3_args, 1, raises=TypeError, a='a', b=2)(6), TypeError),
                              (lambda: check(self.got_3_args, p=1)(7), ValueError),
                             ]:
            with self.assertRaises(errtype):
                calc()


class Test_iterify(unittest.TestCase):
    def setUp(self):
        self.data = OrderedDict(zip(['foo', 'bar', 'baz'], count()))
    def test_retval_equal(self):
        for calc, retval in [(lambda: iterify('foo'), ['foo']),
                             (lambda: iterify('foo', excluded_types={}), 'foo'),
                             (lambda: iterify(['foo']), ['foo']),
                             (lambda: iterify({'foo'}), {'foo'}),
                             (lambda: iterify(self.data), self.data),
                             (lambda: iterify(list(self.data)), list(self.data)),
                             (lambda: iterify(set(self.data)), set(self.data)),
                             (lambda: iterify(tuple(self.data)), tuple(self.data)),
                            ]:
            self.assertEqual(calc(), retval)
    def test_iterator(self):
        iterator = iterify(iter('foo'))
        self.assertIsInstance(iterator, Iterator)
        self.assertFalse(hasattr(iterator, '__len__'))

if __name__ == '__main__':
    unittest.main()
