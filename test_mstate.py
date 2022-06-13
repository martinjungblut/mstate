import unittest
from decimal import Decimal

from mstate import watch


class TestSubtyping(unittest.TestCase):
    types = [list, dict, set, tuple, int, float, Decimal]

    @classmethod
    def test_watched_objects_are_instances_of_original_types(cls):
        for callable in cls.types:
            original = callable()
            watched = watch(original)
            assert isinstance(watched, type(original))


class TestWatchList(unittest.TestCase):
    def setUp(self):
        self.original = []
        self.watched = watch(self.original)

    def test_repr(self):
        self.original.append(10)
        self.watched.append(20)

        assert repr(self.original) == repr(self.watched)

    def test_length(self):
        assert len(self.original) == len(self.watched)

        self.original.append(10)
        self.watched.append(20)

        assert len(self.original) == len(self.watched) == 2

    def test_getitem(self):
        self.original.append(10)
        self.watched.append(20)

        assert self.watched[0] == 10
        assert self.watched[1] == 20
        assert self.watched[-1] == 20

    def test_setitem(self):
        self.original.append(10)
        self.watched.append(20)

        self.original[0] = 1000
        self.watched[1] = 2000

        assert self.watched[0] == 1000
        assert self.original[1] == 2000

    def test_iteration(self):
        self.original.append(10)
        self.watched.append(20)

        assert [i for i in self.watched] == [10, 20]


class TestWatchDict(unittest.TestCase):
    def setUp(self):
        self.original = {}
        self.watched = watch(self.original)

    def test_repr(self):
        self.original["name"] = "john"
        self.watched["age"] = 35

        assert repr(self.original) == repr(self.watched)

    def test_length(self):
        assert len(self.original) == len(self.watched)

        self.original["name"] = "john"
        self.watched["age"] = 35

        assert len(self.original) == len(self.watched) == 2

    def test_setitem_getitem(self):
        self.original["name"] = "john"
        self.watched["age"] = 35

        assert self.watched["name"] == "john"
        assert self.original["age"] == 35

    def test_iteration(self):
        self.original["name"] = "john"
        self.watched["age"] = 35

        {key: value for key, value in self.watched.items()} == {
            "name": "john",
            "age": 35,
        }
