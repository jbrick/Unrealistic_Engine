from Unrealistic_Engine.models.item import Item


class ArmorItem(Item):

    def __init__(self,  name, description, slot, defense_value):
        Item.__init__(self, name, description, slot)
        self.defense_value = defense_value