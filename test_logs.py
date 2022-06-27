import unittest

from mstate import watch


class Player:
    def __init__(self):
        self.inventory = watch([])

    def pick(self, item):
        self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)


def pick(player, item):
    player.pick(item)


class LogsTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_simple_method_calls(self):
        self.player.pick("Sword")
        pick(self.player, "Shield")
        self.player.drop("Shield")

        logs = [*self.player.inventory.ilogs()]

        assert logs[0]["name"] == "append"
        assert logs[0]["value_after"] == "['Sword']"
        assert logs[0]["filename"].endswith("test_logs.py")
        assert logs[0]["linenumber"] == 11

        assert logs[1]["name"] == "append"
        assert logs[1]["value_after"] == "['Sword', 'Shield']"
        assert logs[1]["filename"].endswith("test_logs.py")
        assert logs[1]["linenumber"] == 11

        assert logs[2]["name"] == "remove"
        assert logs[2]["value_after"] == "['Sword']"
        assert logs[2]["filename"].endswith("test_logs.py")
        assert logs[2]["linenumber"] == 14
