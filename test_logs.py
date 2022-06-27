import unittest

from mstate import watch


class Player:
    def __init__(self):
        self.inventory = watch([])

    def pick(self, item):
        self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)


def pick_indirect(player, item):
    player.pick(item)


def drop_direct_manipulation(player, item):
    player.inventory.remove(item)


class LogsTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_simple(self):
        self.player.pick("Sword")
        self.player.pick("Shield")
        self.player.drop("Sword")

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
        assert logs[2]["value_after"] == "['Shield']"
        assert logs[2]["filename"].endswith("test_logs.py")
        assert logs[2]["linenumber"] == 14

    def test_indirect(self):
        pick_indirect(self.player, "Shield")

        logs = [*self.player.inventory.ilogs()]

        assert logs[0]["name"] == "append"
        assert logs[0]["value_after"] == "['Shield']"
        assert logs[0]["filename"].endswith("test_logs.py")
        assert logs[0]["linenumber"] == 11

    def test_direct_manipulation(self):
        self.player.pick("Sword")
        drop_direct_manipulation(self.player, "Sword")

        logs = [*self.player.inventory.ilogs()]

        assert logs[0]["name"] == "append"
        assert logs[0]["value_after"] == "['Sword']"
        assert logs[0]["filename"].endswith("test_logs.py")
        assert logs[0]["linenumber"] == 11

        assert logs[1]["name"] == "remove"
        assert logs[1]["value_after"] == "[]"
        assert logs[1]["filename"].endswith("test_logs.py")
        assert logs[1]["linenumber"] == 22
