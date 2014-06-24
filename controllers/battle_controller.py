import sys
import pygame
import copy

from pygame.constants import K_RETURN

from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.node_leaf import LeafNode
from Unrealistic_Engine.models.action import Action
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.models.target_window import TargetWindow
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.utils import Utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.controllers.controller import Controller


class BattleController(Controller):

    ACTION_SELECT = "Action Select"
    TARGET_SELECT = "Target Select"
    ENEMY_TURN = "Enemy Turn"

    def __init__(self, model, view, current_map, character_start_position, enemy_name):
        self.model = model
        self.view = view
        self.state = BattleController.ACTION_SELECT
        self.current_map = current_map
        self.character_start_position = character_start_position
        self.current_action = None
        self.enemy = copy.copy(model.enemies[enemy_name])

        # Add Character model
        self.view.add_model(
            self.model.character, BattleView.render_character,
            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), 2)
        self.view.set_visible_model_position(
            self.model.character, Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2))

        #Add Map Model
        self.view.add_model(
            self.current_map.get_map_tile(character_start_position.x_coord,
                                          character_start_position.y_coord),
            BattleView.render_map, Position(0, 0), 1)

        #Add Enemy
        self.view.add_model(
            self.enemy, BattleView.render_enemy, Position(Map.GRID_SIZE/2, 2), 2)

        # Add target window Model and set current target to player
        characters = {'Player': self.model.character,
                      'Enemy': self.enemy}
        self.target_window = TargetWindow(self.model.character, self.state, characters)
        self.view.add_model(self.target_window, BattleView.render_target_window,
                            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), 2)

        # Add action select menu to visible models
        self.action_menu = Menu()
        self.action_menu.set_battle_log("%s Attacked!" % enemy_name)
        self.action_menu.addItem(LeafNode(self.set_attack_action, "Attack"))
        self.action_menu.addItem(LeafNode(LeafNode.testFunc, "Items"))
        self.view.add_model(self.action_menu, BattleView.render_action_menu, 0, View.FOREGROUND)

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
                # Previous item in current menu
                self.action_menu.activeNode -= 1

                # Default behaviour is to wrap around at the end of the menu
                if self.action_menu.activeNode < 0:
                    self.action_menu.activeNode = (self.action_menu.nodeCount - 1)
            if pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s:
                # Next item in current menu
                self.action_menu.activeNode += 1

                # Default behaviour is to wrap around at the end of the menu
                if self.action_menu.activeNode >= self.action_menu.nodeCount:
                    self.action_menu.activeNode = 0
            if pressed_key == K_RETURN:
                print(self.action_menu.nodes[self.action_menu.activeNode])
                self.action_menu.nodes[self.action_menu.activeNode].action()

        if pressed_key == pygame.K_b:
            self.end_battle()

        if pressed_key == pygame.K_ESCAPE:
            base = Utils.fetch(Utils.qualify_controller_name(
                "menu_controller"))

            imports = base.MenuController.get_imports()

            view_module = Utils.fetch(imports[base.MenuController.VIEWS] ["main_menu"])

            model = base.MenuController.build_menu()
            view = view_module.MainMenu()
            controller = base.MenuController(model, view, self, self.view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))

    def handle_player_start_point(self, pressed_key):
        if pressed_key == pygame.K_UP or pressed_key == pygame.K_w:
            self.update_target_window(self.enemy, self.state)

    def handle_enemy_start_point(self, pressed_key):
        if pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s:
            self.update_target_window(self.model.character, self.state)

    def update_target_window(self, new_target_model, battle_state):
        # Remove outdated target window from visible models
        self.view.remove_model(self.target_window)

        # Update target window with new target model and/or battle state
        self.target_window.current_target = new_target_model
        self.target_window.battle_state = battle_state

        # Get new target's position
        new_target_position = self.view.get_visible_model_position(new_target_model)

        # Re-add to visible models with new position
        self.view.add_model(self.target_window, BattleView.render_target_window,
                            new_target_position, 2)

    def update_battle_log(self, message):
        self.view.remove_model(self.action_menu)
        self.action_menu.set_battle_log(message)
        self.view.add_model(self.action_menu, BattleView.render_action_menu, 0, View.FOREGROUND)

    def set_attack_action(self):
        self.current_action = Action(Action.ATTACK, self.model.character.attack)
        self.state = BattleController.TARGET_SELECT
        self.update_target_window(self.enemy, self.state)

    def execute_action(self, action):
        if action.type is Action.ATTACK:
            self.target_window.current_target.health -= action.action_arg
            self.update_battle_log("You hit %s for %d damage." %
                                   (self.target_window.current_target.name, action.action_arg))

            # End battle when someone dies
            if self.target_window.current_target.health <= 0:
                if self.target_window.current_target.name == 'Player':
                    self.quit_game()
                else:
                    # return to ensure enemy doesn't attack after being killed
                    self.end_battle()
                    return

            self.state = BattleController.ENEMY_TURN
            self.update_target_window(self.target_window.current_target, self.state)
            self.execute_enemy_turn()

    def execute_enemy_turn(self):
        self.model.character.health -= self.enemy.attack
        self.update_battle_log("%s hit you for %d damage." % (self.enemy.name, self.enemy.attack))
        if self.model.character.health <= 0:
            self.quit_game()

        self.state = BattleController.ACTION_SELECT
        self.update_target_window(self.target_window.current_target, self.state)

    def end_battle(self):
        base = Utils.fetch(Utils.qualify_controller_name("game_controller"))

        imports = base.GameController.get_imports()

        view_module = Utils.fetch(imports[base.GameController.VIEWS]["game_view"])

        view = view_module.GameView()

        # Just give the game view the same visible models as the battle
        # view for now.
        view.visible_models = self.view.visible_models

        controller = base.GameController(self.model, view, self.character_start_position,
                                         self.current_map)

        pygame.event.post(pygame.event.Event(
            event_types.UPDATE_GAME_STATE,
            {"Controller": controller, "View": view}))

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()