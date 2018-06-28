
'''
======
mixins
======

Class decorators and mixin classes

'''
from operator import eq, ne, gt, lt, ge, le

from drytools.annotation.composition import compose_annotations
from drytools.annotation.functions import check


@compose_annotations
def ordered_by(*attrs: check(isinstance, str, raises=TypeError)):
    '''
    Class decorator factory for adding comparison methods based on one or more attributes

    Args:
        attrs (str): Name(s) of attribute(s) to use for ordering

    Returns:
        func: Function to add comparison methods to the class

    Example:
        >>> @ordered_by('name')
        ... class my_cls:
        ...     def __init__(self, name):
        ...        self.name = name
        ...     def __repr__(self):
        ...         return '{}({})'.format(type(self).__name__, repr(self.name))
        >>> sorted([my_cls('foo'), my_cls('bar'), my_cls('bax')])
        [my_cls('bar'), my_cls('bax'), my_cls('foo')]
    '''
    if not attrs:
        raise TypeError('No attrs')
    def comp_val(instance):
        return tuple(getattr(instance, attr) for attr in attrs)
    def decorator(cls):
        def add_comparison_method(comparison):
            method_name = '__{comparison.__name__}__'.format(**locals())
            fun = lambda self, other: comparison(comp_val(self), comp_val(other))
            setattr(cls, method_name, fun)
        for comparison in [eq, ne, gt, lt, ge, le]:
            add_comparison_method(comparison)
        return cls
    return decorator


if __name__ == '__main__':
    import doctest
    doctest.testmod()
