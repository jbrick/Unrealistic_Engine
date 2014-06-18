class TargetWindow():

    def __init__(self, current_target, battle_state):
        self.current_target = current_target
        self.battle_state = battle_state

    def update_current_target(self, current_target, battle_state):
        self.current_target = current_target
        self.battle_state = battle_state
