from inspect import signature
from functools import wraps
from abc import ABC, abstractmethod


class PyTypeValidator(ABC):
    @abstractmethod
    def validate(self, value) -> bool:
        pass


def _any_type_in(input_value, target_type):
    if isinstance(target_type, PyTypeValidator):
        return target_type.validate(input_value)
    else:
        return any(target_type == t for t in type(input_value).mro()[:-1])


def _name_value_annotation(bound_arguments, signature):
    return (
        (
            parameter.name,
            bound_arguments.arguments[parameter.name],
            parameter.annotation,
        )
        for parameter in signature.parameters.values()
    )


def pytype(f):
    """
    Validate the arguments of the supplied function with its annotations.
    """
    f_signature = signature(f)

    @wraps(f)
    def _pytype(*args, **kwargs):
        nonlocal f
        nonlocal f_signature
        bound_arguments = f_signature.bind(*args, **kwargs)
        argument_errors = []
        for name, value, annotation in _name_value_annotation(
            bound_arguments, f_signature
        ):
            if not _any_type_in(value, annotation):
                argument_errors.append(
                    f'Argument {name}("{annotation}") does not match any of {type(value).mro()[:-1]}!'
                )
        if argument_errors:
            raise TypeError("\n".join(argument_errors))
        result = f(*args, **kwargs)
        return result

    return _pytype


class NotZero(PyTypeValidator):
    """
    Validate that a value is an int or a float and that it is not zero
    """

    def validate(self, value):
        return (isinstance(value, int) or isinstance(value, float)) and value != 0


class HasAttr:
    """
    Give a string identifier for an attribute that the field requires
    """

    def __init__(self, attr):
        self.attr = attr

    def __eq__(self, other):
        return self.attr in dir(other)

    def __str__(self):
        return "HasAttr('{}')".format(self.attr)

    __repr__ = __str__


class NotNone:
    """
    Not None
    """

    def __eq__(self, other):
        return other != type(None)

    def __str__(self):
        return "NotNone"

    __repr__ = __str__
