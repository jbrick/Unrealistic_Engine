import json

class Trigger:

    CHANGE_MAP = 1

    def __init__(self, chance, action_type, action_data):
        self.chance = chance
        self.action_type = action_type
        self.action_data = json.loads(action_data)