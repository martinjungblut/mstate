import unittest

from mstate import watch


class Context:
    def __init__(self, logs):
        self.items = watch([], logs=logs)

    def __repr__(self):
        return repr(self.__dict__)


class InheritanceTestCase(unittest.TestCase):
    def setUp(self):
        self.logs = []
        self.instance = watch(Context(self.logs), logs=self.logs)

    def test_nested_method_call(self):
        self.instance.items.append(15)
        self.instance.items.append(25)
        assert len([*self.instance.ilogs()]) == 2
        assert self.logs[0]["name"] == "append"
        assert self.logs[0]["value_after"] == "[15]"
        assert self.logs[1]["name"] == "append"
        assert self.logs[1]["value_after"] == "[15, 25]"

        self.instance.website = "http://debian.org"
        assert len([*self.instance.ilogs()]) == 4
