__author__ = 'steve'


class Item():

    # Item type enums
    Weapon = 0
    Armor = 1
    Healing = 2

    # Slot type enums
    Bag = 0
    LeftHand = 1
    Head = 2

    def __init__(self, name, description, slot):
        self.name = name
        self.description = description
        self.slot = slot

    @staticmethod
    def use_item(self):
        raise NotImplementedError("Please implement this method")