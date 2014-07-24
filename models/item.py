class Item():

    # Item type enums
    Weapon = "Weapon"
    Armor = "Armor"
    Healing = "Healing"

    # Slot type enums
    Bag = "Bag"
    LeftHand = "Left Hand"
    RightHand = "Right Hand"
    Head = "Head"
    Chest = "Chest"
    Legs = "Legs"
    Boots = "Boots"
    Gloves = "Gloves"

    def __init__(self, item_id, name, description, slot):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.slot = slot

    def update_stats(self, old_item, new_item, character):
        raise NotImplementedError("Please implement this method")

    def equip_item(self, character):
        raise NotImplementedError("Please implement this method")

    def unequip_item(self, character):
        raise NotImplementedError("Please implement this method")
