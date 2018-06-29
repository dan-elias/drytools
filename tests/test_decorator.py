
'''
===============================
Unit tests for module decorator
===============================

Unit tests for decorator
'''
import random
import unittest
from drytools.decorator import args2attrs
from drytools.annotation.composition import compose_annotations
from drytools.annotation.functions import iterify
from drytools.decorator import ordered_by



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

class Test_ordered_by(unittest.TestCase):
    def setUp(self):
        random.seed(0)
    def test_normal(self):
        @ordered_by('num1', 'num2')
        class my_cls:
            def __init__(self, num1, num2):
                self.num1, self.num2 = num1, num2
        def shuffled(size=100):
            return random.choices(list(range(size//2)), k=size)
        instances = [my_cls(num1, num2) for num1, num2 in zip(shuffled(), shuffled())]
        sorted_num1 = sorted(x.num1 for x in instances)
        sorted_num2 = sorted(x.num2 for x in instances)
        num2_from_sorted_pairs = [n2 for _, n2 in sorted((x.num1, x.num2) for x in instances)]
        sorted_instances = sorted(instances)
        sorted_instances_num1 = [x.num1 for x in sorted_instances]
        sorted_instances_num2 = [x.num2 for x in sorted_instances]
        self.assertEqual(sorted_num1, sorted_instances_num1)
        self.assertEqual(num2_from_sorted_pairs, sorted_instances_num2)
        self.assertNotEqual(sorted_num2, sorted_instances_num2)
    def test_no_parentheses(self):
        with self.assertRaises(TypeError):
            @ordered_by
            class my_cls:
                pass
    def test_raises_TypeError(self):
        for args in [(1,), ()]:
            with self.assertRaises(TypeError):
                ordered_by(*args)


if __name__ == '__main__':
    unittest.main()
