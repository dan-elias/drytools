
'''
============================
Unit tests for module mixins
============================

Unit tests for mixins
'''
import random
import unittest
from drytools.mixins import ordered_by

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
