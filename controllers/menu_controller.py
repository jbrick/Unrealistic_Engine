import sys
import pygame
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.database import Database


class MenuController(Controller):

    def __init__(self, model, view):
        self.game_model = model
        self.view = view

        self.menu_model = Menu()

        self.menu_model.nodes.append(
            LeafNode("Quit", utils.quit))
        self.menu_model.nodes.append(
            LeafNode("Save Game", Database().save_game, self.game_model.create_memento("test")))
        self.menu_model.nodes.append(
            LeafNode("Load Saved Game", Database().load_saved_game, "test"))

        view.add_model(self.menu_model, MainMenu.render_menu, 0, View.BACKGROUND)

        active_menu = self.menu_model

    def on_leaf_activated(self, node):
        result = node.execute_action()

        if node.label == "Load Saved Game":
            self.game_model.set_memento(result)
            self._return_to_game()

        if node.label == "Save_Game":
            self._return_to_game()


    @staticmethod
    def get_imports():
        models = ["menu", "node_menu", "node_leaf"]
        views = ["main_menu"]
        controllers = ["menu_controller"]
        
        return Controller.qualify_imports((models, views, controllers))

    def handle_key_press(self, pressed_key):

        active_node = self.menu_model.get_active_node()
        if pressed_key == pygame.K_LEFT:
            if len(Menu.breadcrumbs) > 0:
                # Go to previous menu
                self.view.remove_model(self.menu_model)
                self.menu_model = Menu.breadcrumbs.pop();
                self.view.add_model(self.menu_model, MainMenu.render_menu, 0, View.BACKGROUND)
        if pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN:
            if not active_node.is_leaf_node():
                # Traverse into submenu
                Menu.breadcrumbs.append(self.menu_model)
                self.view.remove_model(self.menu_model)
                self.menu_model = active_node.submenu
                self.view.add_model(self.menu_model, MainMenu.render_menu, 0,View.BACKGROUND)
            else:
                # Activate action associate with menu item
                self.on_leaf_activated(active_node)

        if pressed_key == pygame.K_UP:
            # Previous item in current menu
            self.menu_model.active_node -= 1
            
            # Default behaviour is to wrap around at the end of the menu
            if self.menu_model.active_node < 0:
                self.menu_model.active_node = len(self.menu_model.nodes) - 1

        if pressed_key == pygame.K_DOWN:
            # Next item in current menu
            self.menu_model.active_node += 1
            
            # Default behaviour is to wrap around at the end of the menu
            if self.menu_model.active_node >= len(self.menu_model.nodes):
                self.menu_model.active_node = 0

        if pressed_key == pygame.K_ESCAPE:
            self._return_to_game()

    def _return_to_game(self):
        base = utils.fetch(utils.qualify_controller_name("game_controller"))

        imports = base.GameController.get_imports()

        view_module = utils.fetch(imports[base.GameController.VIEWS]["game_view"])
        view = view_module.GameView()
        controller = base.GameController(self.game_model, view)

        Menu.breadcrumbs = []

        pygame.event.post(pygame.event.Event(
            event_types.UPDATE_GAME_STATE, {"Controller": controller, "View": view}))

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
