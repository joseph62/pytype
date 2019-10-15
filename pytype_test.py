import unittest
from pytype import pytype, HasAttr, NotNone

class TestPytype(unittest.TestCase):
    def assertNotRaises(self, exception, f, *args, **kwargs):
        error = False
        try:
            f(*args, **kwargs)
        except exception:
            error = True
        assert not error, f'{exception.__name__} was raised by {f.__name__}'

    def test_inheritance(self):
        class A:
            pass
        class B(A):
            pass

        @pytype
        def inheritance_check(a: A,b: A):
            return True
        self.assertNotRaises(TypeError, inheritance_check, B(), A())

    def test_has_attr(self):
        @pytype
        def window(iterable: HasAttr('__iter__'), size: int):
            return list(zip(*([iter(iterable)]*size)))
        self.assertNotRaises(TypeError, window, [1,2], 1)
        self.assertRaises(TypeError, window, 5, 4)

    def test_not_none_raises_error(self):
        @pytype
        def id(thing: NotNone()):
            return thing
        self.assertRaises(TypeError, id, None)

    def test_not_none(self):
        @pytype
        def id(thing: NotNone()):
            return thing
        self.assertRaises(TypeError, id, None)
        self.assertNotRaises(TypeError, id, 1)

    def test_raw_type(self):
        @pytype
        def add(a: int, b: int):
            return a + b
        self.assertNotRaises(TypeError, add, 1, 2)
        self.assertRaises(TypeError, add, 1.0, 2.0)
