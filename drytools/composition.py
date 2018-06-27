
'''
===========
composition
===========

This module defines a decorator for using annotations for function composition

'''
from collections import ChainMap
from collections.abc import Sequence
from functools import reduce, wraps
import inspect
from drytools.decorator import decorator_factory

def check(predicate, exception_type=ValueError):
    '''
    Factory for univariate validation functions
    
    Args:
        predicate (*callable*):  Function returning True if the input value is 
                                 valid, False otherwise.
        exception_type (*callable*): Constructor for :class:`Exception` to 
                                     raise if _predicate_ returns False
    
    Returns:
        func: Identity function (ie: returns the value passed to it) except 
        that it raises *exception_type* if *predicate* returns False 
        when applied to its input value.
            
    Example:
        >>> check_positive = check((0).__lt__)
        >>> check_positive(5)
        5
        >>> check_positive(-5)
        Traceback (most recent call last):
            ...
        ValueError: -5
        
    '''
    def checked_passthrough(x):
        if not predicate(x):
            raise exception_type(x)
        return x
    return checked_passthrough
    
@decorator_factory
def compose_annotations(combine_var_positional=False, combine_var_keyword=False):
    '''
    Decorator to use compose a function with its callable annotations.
    
    Args:
        combine_var_positional (:class:`bool`): Transform VAR_POSIITIONAL 
          arguments (see :class:`inspect.Parameter`) collectively instead 
          of element-wise (the default)
        combine_var_keyword (:class:`bool`): Transform VAR_KEYWORD arguments 
          (see :class:`inspect.Parameter`) collectively instead of 
          element-wise (the default)
    
    Returns:
        func: Original function composed with its callable annotations
    
    A :class:`collections.abc.Sequence` containing only callable
    elements is treated as a pipeline (ie: the raw value is passed to the first
    element, its return value to the second etc.)
    
    Example:
        >>> @compose_annotations
        ... def to_str(x: str):
        ...     return x
        >>> to_str(5)
        '5'
    
    The behaviour of the resulting (wrapped) function is that the "raw" 
    parameters and return value are "passed through" their respective 
    annotations (ie: their values are replaced with those returned from 
    their annotations).  This can be useful for coercion or validation.
    '''
    def decorator(fun):
        passthrough = lambda x:x
        def get_tx(param_or_sig):
            if isinstance(param_or_sig, inspect.Parameter):
                kind = param_or_sig.kind
                annotation = param_or_sig.annotation
            else:
                assert isinstance(param_or_sig, inspect.Signature)
                kind = None
                annotation = param_or_sig.return_annotation
            if annotation is inspect._empty:
                return passthrough
            elif callable(annotation):
                val_tx = annotation
            elif isinstance(annotation, Sequence) and (len(annotation) > 0) and all(map(callable, annotation)):
                val_tx = lambda raw: reduce(function=lambda v, f: f(v), sequence=annotation, initial=raw)
            else:
                return passthrough
            if (kind is inspect._VAR_POSITIONAL) and (not combine_var_positional):
                return lambda args: tuple(map(val_tx, args))
            elif (kind is inspect._VAR_KEYWORD) and (not combine_var_keyword):
                return lambda kwargs: {k: val_tx(v) for k, v in kwargs.items()}
            else:
                return val_tx
        sig = inspect.signature(fun)
        txs = {k: get_tx(v) for k, v in sig.parameters.items()}
        txs[None] = get_tx(sig)
        keys_with_tx = {k for k, f in txs.items() if f is not passthrough}
        if keys_with_tx:
            params_with_tx = keys_with_tx - {None}
            @wraps(fun)
            def wrapped(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                defaults_to_tx = params_with_tx - set(bound.arguments)
                if defaults_to_tx:
                    bound = sig.bind(*args, **dict(ChainMap(kwargs, {k: sig.parameters[k].default for k in defaults_to_tx})))
                tx_args = []
                tx_kwargs = {}
                for k, v in bound.arguments.items():
                    tx_v = txs[k](v)
                    param = sig.parameters[k]
                    if param.kind is inspect._VAR_POSITIONAL:
                        tx_args.extend(tx_v)
                    elif param.kind is inspect._VAR_KEYWORD:
                        tx_kwargs.update(tx_v)
                    elif param.default is inspect._empty:
                        tx_args.append(tx_v)
                    else:
                        assert param.kind in (inspect._KEYWORD_ONLY, inspect._POSITIONAL_OR_KEYWORD)
                        tx_kwargs[k] = tx_v
                return txs[None](fun(*tx_args, **tx_kwargs))
            return wrapped
        else:
            return fun
    return decorator



if __name__ == '__main__':
    import doctest
    doctest.testmod()


