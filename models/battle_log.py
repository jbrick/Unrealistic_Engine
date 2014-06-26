class BattleLog():

    def __init__(self, init_log_item):
        self.battle_log = [init_log_item]

    def add_battle_log_entry(self, log_entry):
        if self.battle_log is None:
            self.battle_log = []
        self.battle_log.append(log_entry)