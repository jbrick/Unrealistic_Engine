from Unrealistic_Engine.models.item import Item


class HealingItem(Item):

    def __init__(self, item_id, name, description, slot, heal_value):
        Item.__init__(self, item_id, name, description, slot)
        self.heal_value = heal_value

    # Currently this type of item is non equippable
    def equip(self, character):
        return

    def unequip(self, character):
        return

    def update_stats(self, old_item, new_item, character):
        return
