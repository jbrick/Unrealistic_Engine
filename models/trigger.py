import json


class Trigger:

    CHANGE_MAP = 1
    START_BATTLE = 2
    SHOW_DIALOG = 3

    def __init__(self, chance, action_type, triggered_on, action_data):
        self.chance = chance
        self.action_type = action_type
        self.triggered_on = triggered_on
        self.action_data = json.loads(action_data)
