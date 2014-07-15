import sys
import pygame

from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.title_screen_view import TitleScreenView
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu_node import MenuNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.database import Database


class TitleScreenController(Controller):

    def __init__(self, model, view):
        self.game_model = model
        self.view = view
        self.save_node_ids = []
        self.load_node_ids = []

        self.menu_model = Menu(self.view, TitleScreenView.render_menu,
                               self.on_node_activated, Position(0,0))

        new_game_node = LeafNode("New Game", self._return_to_game)
        self.menu_model.nodes.append(new_game_node)
        self.new_game_node_id = new_game_node.id

        load_game_node = MenuNode("Load Saved Game")
        self.menu_model.nodes.append(load_game_node)
        self.load_game_node_id = load_game_node.id

        self.menu_model.nodes.append(
            LeafNode("Quit", utils.quit))


    # Builds a menu object containing all saved games in the database. Each saved game
    # has an action associated with it. Also returns the ids of the created nodes.
    def _build_list_of_saved_games(self, parent, action, action_args):
        game_menu = Menu(self.view, MainMenu.render_menu,
                         self.on_node_activated, Position(0,0))
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

        # Add load game nodes to menu it allows a user to load any existing save.
        if node.id == self.load_game_node_id:
            saved_games_menu = self._build_list_of_saved_games(
                node, Database().load_saved_game, None)
            self.load_node_ids = saved_games_menu[1]
            node.submenu = saved_games_menu[0]

        # If user has selected new game
        if node.id == self.new_game_node_id:
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
