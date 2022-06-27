import unittest
from random import randint

from mstate import watch


class ClassMethodsTestCase(unittest.TestCase):
    class C:
        state = []

        @classmethod
        def add_random_number(cls):
            cls.state.append(randint(1, 10000))

    @classmethod
    def test(cls):
        instance = cls.C()
        watched = watch(instance)

        watched.add_random_number()
        assert len(cls.C.state) == 1

        watched.add_random_number()
        assert len(cls.C.state) == 2
