
'''
==================================
decorator - Some useful decorators
==================================

'''
from collections import ChainMap
from functools import wraps
from operator import eq, ne, gt, lt, ge, le
import inspect

from drytools.annotation.composition import compose_annotations
from drytools.annotation.functions import check, iterify
from drytools.decorator_factory import decorator_factory

@decorator_factory
@compose_annotations
def args2attrs(restrict_to:(iterify, set)=(), 
               exclude:(iterify, set)=(), 
               expand_kw=True):
    '''
    Decorator to copy method arguments to instance attributes that have the
    same names (eg: in __init__)

    Args:
        restrict_to (:class:`str` or iterable): if specified, only include these named arguments
        exclude (:class:`str` or iterable): names of arguments to exclude from copying (even if they're in *include*)
        expand_kw (bool): make an individual attribute for each variable keyword argument

    Returns:
        func: decorator

    Example:
        >>> class my_cls:
        ...     @args2attrs
        ...     def __init__(self, a, b):
        ...         self.total = self.a + self.b
        >>> inst = my_cls(5,2)
        >>> inst.a, inst.b, inst.total
        (5, 2, 7)
    '''
    class to_replace_with_empty_dict:
        pass
    def decorator(fun):
        sig = inspect.signature(fun)
        params_to_copy = set(list(sig.parameters)[1:]) - exclude
        if restrict_to:
            params_to_copy &= restrict_to
        if not params_to_copy:
            raise ValueError('No eligible parameters')
        def name_and_adjusted_default(param):
            default = param.default
            if default is inspect._empty:
                if param.kind is inspect._VAR_POSITIONAL:
                    default = ()
                elif param.kind is inspect._VAR_KEYWORD:
                    default = to_replace_with_empty_dict
            return param.name, default
        defaults = {k:v for k, v in map(name_and_adjusted_default, sig.parameters.values())
                    if (k in params_to_copy) and (v is not inspect._empty)}
        if expand_kw:
            var_kw_params = {p.name for p in sig.parameters.values() if p.kind is inspect._VAR_KEYWORD}  # size 1 or 0
            expand_param = lambda param_name: param_name in var_kw_params
        else:
            expand_param = lambda param_name: False
        @wraps(fun)
        def wrapped(self, *args, **kwargs):
            for name, value in ChainMap(sig.bind(self, *args, **kwargs).arguments, defaults).items():
                if name in params_to_copy:
                    if value is to_replace_with_empty_dict:
                        value = {}
                    if expand_param(name):
                        for k, v in value.items():
                            setattr(self, k, v)
                    else:
                        setattr(self, name, value)
            return fun(self, *args, **kwargs)
        return wrapped
    return decorator

@compose_annotations
def ordered_by(*attrs: check(isinstance, str, raises=TypeError)):
    '''
    Class decorator factory for adding comparison methods based on one or more attributes

    Args:
        attrs (str): Name(s) of attribute(s) to use for ordering instances

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
