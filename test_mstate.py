from decimal import Decimal
import unittest

from mstate import decorate


class TestSubtyping(unittest.TestCase):
    types = [list, dict, set, tuple, int, float, Decimal]

    @classmethod
    def test_decorated_objects_are_instances_of_original_types(cls):
        for callable in cls.types:
            original = callable()
            decorated = decorate(original)
            assert isinstance(decorated, type(original))


class TestDecorateList(unittest.TestCase):
    def setUp(self):
        self.original = []
        self.decorated = decorate(self.original)

    def test_repr(self):
        self.original.append(10)
        self.decorated.append(20)

        assert repr(self.original) == repr(self.decorated)

    def test_length(self):
        assert len(self.original) == len(self.decorated)

        self.original.append(10)
        self.decorated.append(20)

        assert len(self.original) == len(self.decorated) == 2

    def test_getitem(self):
        self.original.append(10)
        self.decorated.append(20)

        assert self.decorated[0] == 10
        assert self.decorated[1] == 20
        assert self.decorated[-1] == 20

    def test_setitem(self):
        self.original.append(10)
        self.decorated.append(20)

        self.original[0] = 1000
        self.decorated[1] = 2000

        assert self.decorated[0] == 1000
        assert self.original[1] == 2000

    def test_iteration(self):
        self.original.append(10)
        self.decorated.append(20)

        assert [i for i in self.decorated] == [10, 20]
