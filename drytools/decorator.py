
'''
=========
decorator
=========

Tools for making decorators

'''
from collections import ChainMap
from functools import wraps
import inspect

from drytools.annotation.functions import iterify

def decorator_factory(fun):
    '''
    Decorator to make parentheses optional when applying a decorator factory
    which has optional arguments.

    Args:
        fun (func): Function that returns a decorator

    Returns:
        func: Decorator factory which, if it is called with a single callable parameter, returns a wrapped function instead of a decorator

    .. important::

        The factory's signature should:

            * Allow it to be called with no arguments
            * *Not* allow it to be called with a single
              positional argument that is callable.
    Example:
        >>> from functools import wraps
        >>> @decorator_factory
        ... def print_when_called(print_done=False):
        ...     def decorator(fun):
        ...         @wraps(fun)
        ...         def wrapped(*args, **kwargs):
        ...             print('calling {}'.format(fun.__name__))
        ...             retval = fun(*args, **kwargs)
        ...             if print_done:
        ...                 print('done')
        ...             return retval
        ...         return wrapped
        ...     return decorator
        >>> @print_when_called(print_done=True)  # decorated with args
        ... def my_fun_print_done():
        ...     pass
        >>> @print_when_called()  # decorated with parentheses, no args
        ... def my_fun_decorated_empty_parentheses():
        ...     pass
        >>> @print_when_called  # decorated without parentheses
        ... def my_fun_decorated_no_parentheses():
        ...     pass
        >>> my_fun_print_done()
        calling my_fun_print_done
        done
        >>> my_fun_decorated_empty_parentheses()
        calling my_fun_decorated_empty_parentheses
        >>> my_fun_decorated_no_parentheses()
        calling my_fun_decorated_no_parentheses
    '''
    @wraps(fun)
    def decorator_or_decorated_function(*args, **kwargs):
        if (not kwargs) and (len(args) == 1) and callable(args[0]):
            return fun()(*args, **kwargs) # decorated_function
        else:
            return fun(*args, **kwargs) # decorator
    return decorator_or_decorated_function

@decorator_factory
def args2attrs(restrict_to=(), exclude=(), expand_kw=True):
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
    restrict_to = set(iterify(restrict_to))
    exclude = set(iterify(exclude))
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
