import json

from Unrealistic_Engine.models.character import Character


class Trigger:

    # Trigger Types
    CHANGE_MAP = "change_map"
    START_BATTLE = "start_battle"
    SHOW_DIALOG = "show_dialog"

    # Triggered On Types
    ENTER = "enter"
    EXIT = "exit"
    KEY_ACTION = "action_key"

    # Trigger Character Directions
    DIRECTION_UP = Character.UP
    DIRECTION_DOWN = Character.DOWN
    DIRECTION_LEFT = Character.LEFT
    DIRECTION_RIGHT = Character.RIGHT
    DIRECTION_ANY = "any"

    def __init__(self, chance, action_type, triggered_on, direction_facing,
                 one_time, action_data):
        self.chance = chance
        self.action_type = action_type
        self.triggered_on = triggered_on
        self.direction_facing = direction_facing
        self.is_one_time = one_time
        self.action_data = json.loads(action_data)
        self.is_active = True
