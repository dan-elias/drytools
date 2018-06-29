
'''
===============================================
decorator_factory - Tools for making decorators
===============================================
'''
from functools import wraps

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



if __name__ == '__main__':
    import doctest
    doctest.testmod()


