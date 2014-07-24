from Unrealistic_Engine.models.item import Item


class WeaponItem(Item):

    def __init__(self, item_id, name, description, slot, attack_value):
        Item.__init__(self, item_id, name, description, slot)
        self.attack_value = attack_value

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
            character.attack -= old_item.attack_value
        if new_item is not None:
            character.attack += new_item.attack_value

