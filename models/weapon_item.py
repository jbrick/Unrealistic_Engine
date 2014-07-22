from Unrealistic_Engine.models.item import Item


class WeaponItem(Item):

    def __init__(self, item_id, name, description, slot, attack_value):
        Item.__init__(self, item_id, name, description, slot)
        self.attack_value = attack_value
