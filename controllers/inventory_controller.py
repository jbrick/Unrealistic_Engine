import pygame
import sys

from Unrealistic_Engine.controllers.controller import Controller

from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.views.inventory_view import InventoryView
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu_node import MenuNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine import event_types


class InventoryController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Add Inventory to visible models
        self.view.add_model(
            self.model.character.inventory, InventoryView.render_inventory,
            Position(0, 0), View.BACKGROUND)

        # Build item list from model into a menu
        self.inventory_menu = Menu(self.view, InventoryView.render_inventory_menu,
                                   self.on_node_activated)

        for item in self.model.character.inventory.item_list:
            self.inventory_menu.nodes.append(
                LeafNode(item.name, self.select_item, item))

    def handle_key_press(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            if len(Menu.breadcrumbs) > 0:
                self.inventory_menu = self.inventory_menu.go_to_previous_menu()

        if pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN:
            self.inventory_menu = self.inventory_menu.activate_node()

        if pressed_key == pygame.K_UP:
            self.inventory_menu.dec_active_node()

        if pressed_key == pygame.K_DOWN:
            self.inventory_menu.inc_active_node()

        if pressed_key == pygame.K_i:
            # For now goes back to only game controller, but we need a
            # way to detect previous controller
            self.close_inventory()

    def on_node_activated(self, node):
        if node.is_leaf_node():
            node.execute_action()

    def select_item(self, item):
        print("Item %s was selected." % item[0].name)

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