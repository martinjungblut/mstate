import unittest

from mstate import watch


@watch
class Inventory(list):
    def instance_watch(self):
        return repr(self)


@watch
class Player:
    class_inventory = Inventory()

    def __init__(self, name):
        self.inventory = Inventory()
        self.name = name

    def instance_watch(self):
        return repr(self.__dict__)

    @classmethod
    def class_watch(cls):
        return repr({"class_inventory": cls.class_inventory})

    def pick(self, item):
        self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)

    @classmethod
    def class_pick(cls, item):
        cls.class_inventory.append(item)


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player("Jack")

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


global_inventory = Inventory()
global_inventory.append("Amulet")


class GlobalInstanceTestCase(unittest.TestCase):
    def test(self):
        global_inventory.append("Rune")
        global_inventory.append("Mug")

        logs = [*global_inventory.ilogs()]
        assert len(logs) > 0
        print("Global inventory logs")
        for log in logs:
            print(log)
