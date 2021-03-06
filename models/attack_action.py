from Unrealistic_Engine.models.action import Action


class AttackAction(Action):

    def __init__(self, attacker_power):
        self.attacker_power = attacker_power

    def execute_action(self, target_window, battle_log, *args, **kwargs):
        if target_window.current_target.defense >= self.attacker_power:
            battle_log.add_battle_log_entry("Your attack was dodged!")
        else:
            target_window.current_target.health -= (self.attacker_power - target_window.
                                                    current_target.defense)
            battle_log.add_battle_log_entry("You hit %s for %d damage." %
                                            (target_window.current_target.name,
                                             self.attacker_power - target_window.
                                             current_target.defense))
