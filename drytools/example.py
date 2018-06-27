'''
==============
Example module
==============

This module is not part of the project.  It is here to serve as a style
example and the subject of example unit tests.

Docstrings are based on `this example <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_

Unit tests for this module are in: ../tests/test_example.py

'''


def str_repeat(s, n=1):
    '''
    Example function that repeats a string a number of times

    Args:
        s (str): string to repeat
        n (int): number of repetitions

    Returns:
        str: s repeated n times

    Raises:
        TypeError: `s` not a string, or `n` not an integer
        ValueError: `n` negative

    Example:
        >>> str_repeat('a', 3)
        'aaa'
        >>> str_repeat('and_again_', 3)
        'and_again_and_again_and_again_'
        >>> str_repeat('x', -1)
        Traceback (most recent call last):
        ...
        ValueError: n negative
    '''
    for name, val, typ in [('s', s, str), ('n', n, int)]:
        if not isinstance(val, typ):
            raise TypeError('{name} not of type {typ.__name__}'.format(**locals()))
        if n < 0:
            raise ValueError('n negative')
    return s * n

if __name__ == '__main__':
    import doctest
    doctest.testmod()
