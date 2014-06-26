import sys
import pygame
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu_node import MenuNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.database import Database


class MenuController(Controller):

    def __init__(self, model, view):
        self.game_model = model
        self.view = view
        self.save_node_ids = []
        self.load_node_ids = []

        self.menu_model = Menu()

        self.menu_model.nodes.append(
            LeafNode("Quit", utils.quit))

        save_game_node = MenuNode("Save Game")
        self.menu_model.nodes.append(save_game_node)
        self.save_game_node_id = save_game_node.id

        load_game_node = MenuNode("Load Saved Game")
        self.menu_model.nodes.append(load_game_node)
        self.load_game_node_id = load_game_node.id

        view.add_model(self.menu_model, MainMenu.render_menu, 0, View.BACKGROUND)

        active_menu = self.menu_model

    # Builds a menu object containing all saved games in the database. Each saved game
    # has an action associated with it. Also returns the ids of the created nodes.
    def _build_list_of_saved_games(self, parent, action, action_args):
        game_menu = Menu()
        game_ids = Database().get_saved_games()
        node_ids = []
        for id in game_ids:
            new_node = LeafNode("Game "+ str(id), action, id, action_args)
            node_ids.append(new_node.id)
            game_menu.nodes.append(new_node)

        return game_menu, node_ids

    def on_node_activated(self, node):

        if node.is_leaf_node():
            result = node.execute_action()

        # Add save game nodes to menu it consists of allowing the user to overwrite any
        # existing save or add a new one.
        if node.id == self.save_game_node_id:
            saved_games_menu = self._build_list_of_saved_games(
                node, Database().save_game_overwrite, self.game_model.create_memento())
            self.save_node_ids = saved_games_menu[1]

            new_node = LeafNode(
                "New Saved Game", Database().save_game, self.game_model.create_memento())
            saved_games_menu[0].nodes.append(new_node)
            self.save_node_ids.append(new_node.id)
            node.submenu = saved_games_menu[0]

        # Add load game nodes to menu it allows a user to load any existing save.
        if node.id == self.load_game_node_id:
            saved_games_menu = self._build_list_of_saved_games(
                node, Database().load_saved_game, None)
            self.load_node_ids = saved_games_menu[1]
            node.submenu = saved_games_menu[0]

        # If user has selected a save node
        if node.id in self.save_node_ids:
            self._return_to_game()

        # If user has selected a load node
        if node.id in self.load_node_ids:
            self.game_model.set_memento(result)
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
            self.on_node_activated(active_node)
            if not active_node.is_leaf_node():
                # Traverse into submenu
                Menu.breadcrumbs.append(self.menu_model)
                self.view.remove_model(self.menu_model)
                self.menu_model = active_node.submenu
                self.view.add_model(self.menu_model, MainMenu.render_menu, 0,View.BACKGROUND)

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
