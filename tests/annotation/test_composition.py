
'''
============================================
Unit tests for module annotation.composition
============================================

Unit tests for annotation.composition
'''
import unittest
from drytools.annotation.composition import compose_annotations

class Test_compose_annotations(unittest.TestCase):
    def test_coerce_params(self):
        @compose_annotations
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
        @compose_annotations
        def f(x) -> str:
            return x
        for args, kwargs in [((1,), {}),
                             (('a',),  {}),
                             ((),  {'x':1}),
                             ((),  {'x':'a'}),
                             ]:
            self.assertIsInstance(f(*args, **kwargs), str)
    def test_pipeline(self):
        @compose_annotations
        def f(x:(int, str)):
            return x
        self.assertEqual(f(3.14), '3')
    def test_combine_var_positional(self):
        @compose_annotations(combine_var_positional=True, combine_var_keyword=False)
        def f(x, *args:set, y:int=10, **kwargs:str):
            return x, args, y, sorted(kwargs.items())
        self.assertEqual(f(1, 2, 3, 2, 3, 2, 3, 2, 3, t=1, u=2, v=3), (1, (2, 3), 10, [('t', '1'), ('u', '2'), ('v', '3')]))
    def test_combine_var_keyword(self):
        @compose_annotations(combine_var_positional=False, combine_var_keyword=True)
        def f(x, *args:str, y:int=10, **kwargs:(lambda d: {k: v*2 for k, v in d.items()})):
            return x, args, y, sorted(kwargs.items())
        self.assertEqual(f(1, 2, 3, 2, 3, 2, 3, 2, 3, t=1, u=2, v=3), (1, ('2', '3', '2', '3', '2', '3', '2', '3'), 10, [('t', 2), ('u', 4), ('v', 6)]))
    def test_application_to_method(self):
        class my_cls:
            @compose_annotations
            def __init__(self, x:str):
                self.x = x
        self.assertIsInstance(my_cls(10).x, str)
        


if __name__ == '__main__':
    unittest.main()
