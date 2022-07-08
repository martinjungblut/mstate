import unittest

from mstate import watch


@watch
class Inventory(list):
    pass


@watch
class Player:
    class_inventory = Inventory()

    def __init__(self):
        self.inventory = Inventory()

    def __repr__(self):
        return "inventory={}, class_inventory={}".format(
            repr(self.inventory), repr(self.class_inventory)
        )

    def pick(self, item):
        self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)

    @classmethod
    def class_pick(cls, item):
        cls.class_inventory.append(item)


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test(self):
        self.player.pick("Sword")
        self.player.pick("Shield")
        self.player.drop("Shield")

        self.player.class_pick("Backpack")
        self.player.class_pick("Torch")

        logs = [*self.player.ilogs()]
        assert len(logs) > 0
        print("Player logs")
        for log in logs:
            print(log)

        logs = [*self.player.inventory.ilogs()]
        assert len(logs) > 0
        print("Inventory logs")
        for log in logs:
            print(log)
