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
        if item not in self.inventory:
            self.inventory.append(item)

    def drop(self, item):
        self.inventory.remove(item)

    def reset(self):
        self.inventory = Inventory()

    @classmethod
    def class_pick(cls, item):
        cls.class_inventory.append(item)
