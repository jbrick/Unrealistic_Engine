from Unrealistic_Engine.views.view import View


class BattleViewInterface(View):

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_enemy(enemy, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_target_window(target_window, screen, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_action_menu(action_menu, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")