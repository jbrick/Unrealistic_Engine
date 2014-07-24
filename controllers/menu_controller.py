import sys
import pygame

from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu_node import MenuNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.database import Database


class MenuController(Controller):

    def __init__(self, model, view, previous_controller, previous_view):
        self.game_model = model
        self.view = view
        self.previous_controller = previous_controller
        self.previous_view = previous_view
        self.save_node_ids = []
        self.load_node_ids = []

        self.menu_model = Menu(
            self.view, MainMenu.render_menu,self.on_node_activated,
            Position(Map.MAP_SIZE/2 - MainMenu.MENU_WIDTH /2, Map.MAP_SIZE/2 -
                     MainMenu.MENU_HEIGHT /2))

        save_game_node = MenuNode("Save Game")
        self.menu_model.nodes.append(save_game_node)
        self.save_game_node_id = save_game_node.id

        load_game_node = MenuNode("Load Saved Game")
        self.menu_model.nodes.append(load_game_node)
        self.load_game_node_id = load_game_node.id

        self.menu_model.nodes.append(LeafNode("Quit", utils.quit))

    def on_node_activated(self, node):

        if node.is_leaf_node():
            result = node.execute_action()

        # Add save game nodes to menu it consists of allowing the user to overwrite any
        # existing save or add a new one.
        if node.id == self.save_game_node_id:

            game_menu = Menu(self.view, MainMenu.render_menu,
                             self.on_node_activated,Position(
                             Map.MAP_SIZE / 2 - MainMenu.MENU_WIDTH / 2,
                             Map.MAP_SIZE / 2 - MainMenu.MENU_HEIGHT / 2))

            self.save_node_ids = utils.add_saved_game_nodes(
                                 game_menu, Database().save_game_overwrite,
                                 self.game_model.create_memento())

            new_node = LeafNode(
                "New Saved Game", Database().save_game,
                 self.game_model.create_memento())

            game_menu.nodes.append(new_node)
            self.save_node_ids.append(new_node.id)
            node.submenu = game_menu

        # Add load game nodes to menu it allows a user to load any existing save.
        if node.id == self.load_game_node_id:
            game_menu = Menu(self.view, MainMenu.render_menu,
                             self.on_node_activated,Position(
                             Map.MAP_SIZE / 2 - MainMenu.MENU_WIDTH / 2,
                             Map.MAP_SIZE / 2 - MainMenu.MENU_HEIGHT / 2))

            self.load_node_ids = utils.add_saved_game_nodes(
                                game_menu, Database().load_saved_game, None)

            node.submenu = game_menu

        # If user has selected a save node
        if node.id in self.save_node_ids:
            utils.return_to_game(self.game_model)

        # If user has selected a load node
        if node.id in self.load_node_ids:
            self.game_model.set_memento(result)
            utils.return_to_game(self.game_model)

    @staticmethod
    def get_imports():
        models = ["menu", "node_menu", "node_leaf"]
        views = ["main_menu"]
        controllers = ["menu_controller"]
        
        return Controller.qualify_imports((models, views, controllers))

    def handle_key_press(self, pressed_key):

        if pressed_key == pygame.K_LEFT:
            if len(Menu.breadcrumbs) > 0:
                self.menu_model = self.menu_model.go_to_previous_menu()

        if pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN:
            self.menu_model = self.menu_model.activate_node()

        if pressed_key == pygame.K_UP:
            self.menu_model.dec_active_node()

        if pressed_key == pygame.K_DOWN:
            self.menu_model.inc_active_node()

        if pressed_key == pygame.K_ESCAPE:
            utils.return_to_game(self.game_model)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
