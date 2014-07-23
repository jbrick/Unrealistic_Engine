import sys
import pygame
import copy

from pygame.constants import K_RETURN

from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.attack_action import AttackAction
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.models.target_window import TargetWindow
from Unrealistic_Engine.models.battle_log import BattleLog
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.controllers.controller import Controller


class BattleController(Controller):

    ACTION_SELECT = 0
    TARGET_SELECT = 1
    ENEMY_TURN = 2

    def __init__(self, model, view, enemy_name):
        self.model = model
        self.view = view
        self.state = BattleController.ACTION_SELECT
        self.current_action = None
        self.enemy = copy.copy(model.enemies[enemy_name])

        # Add Character model
        self.view.add_model(
            self.model.character, BattleView.render_character,
            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), View.FOREGROUND)

        # Add Map Model
        self.view.add_model(
            self.model.current_map.get_map_tile(self.model.character.position.x_coord,
                                                self.model.character.position.y_coord),
            BattleView.render_map, Position(0, Map.MAP_SIZE -
                                            BattleView.MENU_HEIGHT),
            View.BACKGROUND)

        # Add Enemy
        self.view.add_model(
            self.enemy, BattleView.render_enemy, Position(Map.GRID_SIZE/2, 2), View.FOREGROUND)

        # Add target window Model and set current target to player
        characters = {'Player': self.model.character,
                      'Enemy': self.enemy}
        self.target_window = TargetWindow(self.model.character, self.state, characters)
        self.view.add_model(self.target_window, BattleView.render_target_window,
                            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), View.FOREGROUND)

        # Add action select menu to visible models
        self.action_menu = Menu(
            self.view, BattleView.render_menu,self.on_node_activated,
            Position(0, Map.MAP_SIZE - BattleView.MENU_HEIGHT))

        self.action_menu.nodes.append(LeafNode("Attack", self.set_attack_action))
        self.action_menu.nodes.append(LeafNode("Items", None))

        # Add Battle Log
        self.battle_log = BattleLog("%s Attacked!" % enemy_name)
        self.view.add_model(self.battle_log, BattleView.render_battle_log,
                            Position(0, 0), View.FOREGROUND)

    def on_node_activated(self, node):
        if node.is_leaf_node():
            node.execute_action()

    @staticmethod
    def get_imports():
        models = ["map", "trigger"]
        views = ["battle_view"]
        controllers = ["battle_controller"]

        return Controller.qualify_imports((models, views, controllers))

    def handle_key_press(self, pressed_key):
        if self.state is BattleController.TARGET_SELECT:
            if self.target_window.current_target.name == 'Player':
                self.handle_player_start_point(pressed_key)
            else:
                self.handle_enemy_start_point(pressed_key)

            if pressed_key == K_RETURN:
                self.execute_action(self.current_action)
                self.current_action = None

        elif self.state is BattleController.ACTION_SELECT:
            if pressed_key == pygame.K_UP or pressed_key == pygame.K_w:
                self.action_menu.dec_active_node()
            if pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s:
                self.action_menu.inc_active_node()
            if pressed_key == K_RETURN:
                self.action_menu = self.action_menu.activate_node()

        if pressed_key == pygame.K_b:
            self.end_battle()

    def handle_player_start_point(self, pressed_key):
        if pressed_key == pygame.K_UP or pressed_key == pygame.K_w:
            self.update_target_window(self.enemy, self.state)

    def handle_enemy_start_point(self, pressed_key):
        if pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s:
            self.update_target_window(self.model.character, self.state)

    def update_target_window(self, new_target_model, battle_state):
        # Update target window with new target model and/or battle state
        self.target_window.current_target = new_target_model
        self.target_window.battle_state = battle_state

        # Get new target's position and set it for the target window
        new_target_position = self.view.get_visible_model_position(new_target_model)
        self.view.set_visible_model_position(self.target_window, new_target_position)

    def update_battle_log(self, message):
        self.battle_log.add_battle_log_entry(message)

    def set_attack_action(self):
        self.current_action = AttackAction(self.model.character.attack)
        self.state = BattleController.TARGET_SELECT
        self.update_target_window(self.enemy, self.state)

    def execute_action(self, action):
        action.execute_action(self.target_window, self.battle_log)

        # End battle when someone dies
        if self.target_window.current_target.health <= 0:
            if self.target_window.current_target.name == 'Player':
                self.quit_game()
            else:
                # return to ensure enemy doesn't attack after being killed
                self.end_battle()
                return

        # Change to enemy turn
        self.state = BattleController.ENEMY_TURN

        # Update target window
        self.update_target_window(self.target_window.current_target, self.state)
        self.execute_enemy_turn()

    def execute_enemy_turn(self):

        if self.model.character.defense >= self.enemy.attack:
            self.update_battle_log("You dodged %s's attack." % self.enemy.name)
        else:
            self.model.character.health -= (self.enemy.attack - self.model.character.defense)
            self.update_battle_log("%s hit you for %d damage." % (self.enemy.name, self.enemy.attack))

        if self.model.character.health <= 0:
            self.quit_game()

        self.state = BattleController.ACTION_SELECT
        self.update_target_window(self.target_window.current_target, self.state)

    def end_battle(self):
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

    def quit_game(self):
        pygame.quit()
        sys.exit()
