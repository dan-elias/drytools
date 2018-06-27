import unittest
from drytools import example

class Test_str_repeat(unittest.TestCase):
    def setUp(self):
        self.fun = example.str_repeat
    def test_retval_equal(self):
        for calc, retval in [(lambda: self.fun('a'), 'a'),
                             (lambda: self.fun(''), ''),
                             (lambda: self.fun('hi'), 'hi'),
                             (lambda: self.fun('abc', n=3), 'abcabcabc'),
                             (lambda: self.fun('abc', 0), ''),
                            ]:
            self.assertEqual(calc(), retval)
    def test_TypeError(self):
        for calc in [lambda: self.fun(3),
                     lambda: self.fun(True),
                     lambda: self.fun('a', 'a'),
                     ]:
            with self.assertRaises(TypeError):
                calc()
    def test_ValueError(self):
        for calc in [lambda: self.fun('a', n=-1),
                    ]:
            with self.assertRaises(ValueError):
                calc()

if __name__ == '__main__':
    unittest.main()
