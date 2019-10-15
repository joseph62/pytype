from inspect import signature

def pytype(f):
    # Create a dict of varname to possible types
    f_signature = signature(f)
    def _pytype(*args,**kwargs):
        nonlocal f
        nonlocal f_signature
        # Are any of the possible types in the target type's inheritance?
        def any_type_in(input_type, target_type):
            return any(target_type == t for t in input_type.mro()[:-1])
        def value_annotation(bound_arguments, signature):
            return ((parameter.name, bound_arguments.arguments[parameter.name], parameter.annotation) for parameter in signature.parameters.values())
        # Create a dict of varname to given value
        bound_arguments = f_signature.bind(*args, **kwargs)
        for name, value, annotation in value_annotation(bound_arguments, f_signature):
            if not any_type_in(type(value), annotation):
                raise TypeError("Argument {}('{}') does not match any of {}!".format(
                            name, annotation, list(type(value).mro()[:-1])))
        result = f(*args,**kwargs)
        return result

    return _pytype

class HasAttr:
    """
    Give a string identifier for an attribute that the field requires
    """
    def __init__(self,attr):
        self.attr = attr
    def __eq__(self,other):
        return self.attr in dir(other)
    def __str__(self):
        return "HasAttr('{}')".format(self.attr)
    __repr__ = __str__

class NotNone:
    """
    Not None
    """
    def __eq__(self,other):
        return other != type(None)
    def __str__(self):
        return "NotNone"
    __repr__ = __str__
