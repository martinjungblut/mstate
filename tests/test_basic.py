import pytest

from tests.common import Inventory, Player


class TestBasic:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.player = Player("Jack")

    def test(self):
        self.player.pick("Sword")
        self.player.pick("Shield")
        self.player.drop("Shield")

        self.player.class_pick("Backpack")
        self.player.class_pick("Torch")

        self.player.reset()
        self.player.pick("Sword")

        logs = [*self.player.ilogs()]
        assert len(logs) > 0
        print("Player logs")
        for index, log in enumerate(logs):
            print(index, log)

        logs = [*self.player.inventory.ilogs()]
        assert len(logs) > 0
        print("Inventory logs")
        for index, log in enumerate(logs):
            print(index, log)


global_inventory = Inventory()
global_inventory.append("Amulet")


class TestGlobalInstance:
    def test(self):
        global_inventory.append("Rune")
        global_inventory.append("Mug")

        logs = [*global_inventory.ilogs()]
        assert len(logs) > 0
        print("Global inventory logs")
        for index, log in enumerate(logs):
            print(index, log)
