import pygame
import sys

from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.views.inventory_view import InventoryView
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.utils.position import Position

from Unrealistic_Engine import event_types


class InventoryController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Add Inventory to visible models
        self.view.add_model(
            self.model.character.inventory, InventoryView.render_inventory,
            Position(0, 0), View.FOREGROUND)

    def handle_key_press(self, pressed_key):
        if pressed_key == pygame.K_i:
            # For now goes back to only game controller, but we need a
            # way to detect previous controller
            self.close_inventory()

    def close_inventory(self):
        base = utils.fetch(utils.qualify_controller_name("game_controller"))

        imports = base.GameController.get_imports()

        view_module = utils.fetch(imports[base.GameController.VIEWS]["game_view"])

        view = view_module.GameView()

        controller = base.GameController(self.model, view)

        pygame.event.post(pygame.event.Event(
            event_types.UPDATE_GAME_STATE,
            {"Controller": controller, "View": view}))

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()

    @staticmethod
    def get_imports():
        models = ["map", "trigger"]
        views = ["inventory_view"]
        controllers = ["inventory_controller"]

        return Controller.qualify_imports((models, views, controllers))

    def quit_game(self):
        pygame.quit()
        sys.exit()