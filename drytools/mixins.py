
'''
====================================
mixins - add Python standard methods
====================================
'''
import inspect

class repr_from_init:
    '''
    Mixin that implements __repr__ method based in signature of __init__.
    
    Example:
        >>> from drytools import args2attrs
        >>> class my_cls(repr_from_init):
        ...     @args2attrs
        ...     def __init__(self, a1, *args, k1=8, k2=8):
        ...         pass
        >>> my_cls(1,2,'foo')
        my_cls(1, 2, 'foo')
        >>> my_cls(k2=5, a1=1)
        my_cls(1, k2=5)
    
    Requirements:
        
        * __init__ must not have any variable keyword arguments
        * __init__ arguments (including variable positional ones) must all 
          be saved as instance attribtues with the same names.  An easy 
          way to do this is to use the :func:`args2attrs` decorator.
    '''
    def __repr__(self):
        sig = inspect.signature(self.__init__)
        def _kwarg_repr(name, value):
            value_repr = repr(value)
            return '{name}={value_repr}'.format(**locals())
        arg_reprs = []
        for param in sig.parameters.values():
            param_value = getattr(self, param.name)
            if param.kind is inspect._VAR_POSITIONAL:
                arg_reprs.extend(map(repr, param_value))
            elif param.kind is inspect._VAR_KEYWORD:
                arg_reprs.extend(_kwarg_repr(k, v) for k, v in sorted(param_value.items()))
            elif param.default is not inspect._empty:
                if param_value != param.default:
                    arg_reprs.append(_kwarg_repr(param.name, param_value))
            else:
                assert param.kind in (inspect._POSITIONAL_ONLY, inspect._POSITIONAL_OR_KEYWORD)
                arg_reprs.append(repr(param_value))
        return '{cls_name}({combined_args_repr})'.format(cls_name=type(self).__name__, combined_args_repr=', '.join(arg_reprs))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
