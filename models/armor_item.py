from Unrealistic_Engine.models.item import Item


class ArmorItem(Item):

    def __init__(self,  item_id, name, description, slot, defense_value):
        Item.__init__(self, item_id, name, description, slot)
        self.defense_value = defense_value

    def equip(self, character):
        old_item = None
        if self.slot in character.loadout:
            old_item = character.loadout[self.slot]
        character.loadout[self.slot] = self
        # Show dialog that item was equipped

        self.update_stats(old_item, self, character)

    def unequip(self, character):
        del character.loadout[self.slot]
        self.update_stats(self, None, character)

    def update_stats(self, old_item, new_item, character):
        if old_item is not None:
            character.defense -= old_item.defense_value
        if new_item is not None:
            character.defense += new_item.defense_value

