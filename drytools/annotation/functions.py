
'''
=====================================================
annotation.functions - Coerce and validate parameters
=====================================================

When the :func:`drytools.annotation.composition.compose_annotations` decorator
is used, these functions can he used as annotations to coerce and/or
validate parameters.

'''
from collections.abc import Iterable

'''
Validation
----------
'''
def check(predicate, *args, raises=ValueError, **kwargs):
    '''
    Factory for univariate validation functions

    Args:
        predicate (*callable*):  Function returning True if the input value is
                                 valid, False otherwise.  The value to be
                                 checked is used as the first argument.
                                 Additional (constant) arguments can be supplied
                                 in *args* and *kwargs* (see example).
        raises (*callable*): Constructor for :class:`Exception` to
                             raise if *predicate* returns False
        args, kwargs: additional arguments for predicate

    Returns:
        func: Identity function (ie: returns the value passed to it) except
        that it raises *exception_type* if *predicate* returns False
        when applied to its input value.

    Example:
        >>> from operator import gt
        >>> check_positive = check(gt, 0)
        >>> check_positive(5)
        5
        >>> check_positive(-3)
        Traceback (most recent call last):
            ...
        ValueError: -3

    '''
    def checked_passthrough(x):
        if not predicate(x, *args, **kwargs):
            raise raises(x)
        return x
    return checked_passthrough

'''
Coercion
--------

In addition to the functions below, types (eg: :class:`int`, :class:`str`,
:class:`pathlib.Path`) are useful for coercion.
'''

def iterify(x, excluded_types=str):
    '''
    Coerce to an iterable

    Args:
        x: Object to coerce
        excluded_types (:class:`type` or iterable): one or more types to treat as elements even if they are iterable

    Returns:
        *iterable*: Either *x* (if it's iterable and not one of *excluded_types*) or a single-element list containing *x*


    Example:
        >>> list(iterify('foo'))
        ['foo']
        >>> list(iterify('foo', excluded_types={}))
        ['f', 'o', 'o']
        >>> iterify(['foo', 'bar', 'baz'])
        ['foo', 'bar', 'baz']
    '''
    if not isinstance(excluded_types, Iterable):
        excluded_types = [excluded_types]
    ok = isinstance(x, Iterable) and (not any(isinstance(x, t) for t in excluded_types))
    return x if ok else [x]



if __name__ == '__main__':
    import doctest
    doctest.testmod()
