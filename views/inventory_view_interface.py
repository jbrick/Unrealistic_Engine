from Unrealistic_Engine.views.view import View


class InventoryViewInterface(View):

    @staticmethod
    def render_inventory(inventory, screen, position, *args, **kwargs):
        raise NotImplementedError("Please implement this method")