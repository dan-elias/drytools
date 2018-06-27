
'''
=================================
Unit tests for module composition
=================================

Unit tests for composition
'''

import unittest
from drytools import composition

class Test_compose_annotations(unittest.TestCase):
    def setUp(self):
        self.fun = composition.compose_annotations
    def test_coerce_params(self):
        @self.fun
        def f(w: int, x, y=1, z:str=2):
            return w, x, y, z
        for args, kwargs, expected_types in [((1, 1), {}, (int, int, int, str)),
                                             (('1', '1'),  {}, (int, str, int, str)),
                                             ((1, '1'),  {'z':1}, (int, str, int, str)),
                                             (('1', 1, 'x'), {}, (int, int, str, str)),
                                             ]:
            for val, expected_type in zip(f(*args, **kwargs), expected_types):
                self.assertIsInstance(val, expected_type)
    def test_coerce_retval(self):
        @self.fun
        def f(x) -> str:
            return x
        for args, kwargs in [((1,), {}),
                             (('a',),  {}),
                             ((),  {'x':1}),
                             ((),  {'x':'a'}),
                             ]:
            self.assertIsInstance(f(*args, **kwargs), str)
    def test_combine_var_positional(self):
        @self.fun(combine_var_positional=True, combine_var_keyword=False)
        def f(x, *args:set, y:int=10, **kwargs:str):
            return x, args, y, sorted(kwargs.items())
        self.assertEqual(f(1, 2, 3, 2, 3, 2, 3, 2, 3, t=1, u=2, v=3), (1, (2, 3), 10, [('t', '1'), ('u', '2'), ('v', '3')]))
    def test_combine_var_keyword(self):
        @self.fun(combine_var_positional=False, combine_var_keyword=True)
        def f(x, *args:str, y:int=10, **kwargs:(lambda d: {k: v*2 for k, v in d.items()})):
            return x, args, y, sorted(kwargs.items())
        self.assertEqual(f(1, 2, 3, 2, 3, 2, 3, 2, 3, t=1, u=2, v=3), (1, ('2', '3', '2', '3', '2', '3', '2', '3'), 10, [('t', 2), ('u', 4), ('v', 6)]))



if __name__ == '__main__':
    unittest.main()


