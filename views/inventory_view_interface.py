from Unrealistic_Engine.views.view import View


class InventoryViewInterface(View):

    @staticmethod
    def render_background(model, screen, position, *args, **kwargs):
        raise NotImplementedError("Please implement this method")

    @staticmethod
    def render_inventory_menu(inventory_menu, screen, position, *args, **kwargs):
        raise NotImplementedError("Please implement this method")

    @staticmethod
    def render_description(description, screen, position, *args, **kwargs):
        raise NotImplementedError("Please implement this method")

    @staticmethod
    def render_character_data(character, screen, position, *args, **kwargs):
        raise NotImplementedError("Please implement this method")
