

class Action():

    def __init__(self):
        self.test = None

    @staticmethod
    def execute_action(self, target_window, battle_log, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")