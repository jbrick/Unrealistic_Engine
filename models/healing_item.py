from Unrealistic_Engine.models.item import Item


class HealingItem(Item):

    def __init__(self, item_id, name, description, slot, heal_value):
        Item.__init__(self, item_id, name, description, slot)
        self.heal_value = heal_value