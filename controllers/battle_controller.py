import sys
import os
import pygame
from pygame.constants import K_RETURN

import Unrealistic_Engine.controllers
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.models.target_window import TargetWindow
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.character import Character
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.position import Position


class BattleController(Controller):

    ACTION_SELECT = "Action Select"
    TARGET_SELECT = "Target Select"
    ENEMY = "Enemy Turn"

    def __init__(self, model, view, current_visible_models, current_map, character_start_position):
        self.model = model
        self.view = view
        self.state = self.TARGET_SELECT
        self.current_visible_models = current_visible_models
        self.current_map = current_map
        self.character_start_position = character_start_position
        self.current_action = None

        # Add Character model
        self.view.add_model(
            self.model.character, BattleView.render_character,
            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), 2)
        self.view.set_visible_model_position(
            self.model.character, Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2))

        #Add Map Model
        self.view.add_model(
            self.current_map.get_tile_at_position(character_start_position),
            BattleView.render_map, Position(0, 0), 1)

        #Add test Enemy
        npc_image = pygame.image.load(
            os.path.join('Images', "boss1.png"))
        npc_image_scaled = pygame.transform.scale(
            npc_image, (Character.SIZE, Character.SIZE))
        self.test_npc = Character("Boss1", npc_image_scaled, 100, 10)
        self.view.add_model(
            self.test_npc, BattleView.render_enemy, Position(Map.GRID_SIZE/2, 2), 2)

        # Add target window Model and set current target to player
        self.target_window = TargetWindow(self.model.character)
        self.view.add_model(self.target_window, BattleView.render_target_window,
                            Position(Map.GRID_SIZE/2, Map.GRID_SIZE/2), 2)

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)

        if self.state is BattleController.TARGET_SELECT:
            if self.target_window.current_target.name == 'Player':
                self.handle_player_start_point(pressed_key)
            else:
                self.handle_enemy_start_point(pressed_key)

            if pressed_key == K_RETURN:
                #self.execute_action()
                self.current_action = None

        #elif self.state is BattleController.ACTION_SELECT:


        

        #elif state is ENEMY:


        #if pressed_key == pygame.K_LEFT:

        #if pressed_key == pygame.K_RIGHT:

        #if pressed_key == pygame.K_UP:

        #if pressed_key == pygame.K_DOWN:

        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_b:
            view = GameView()
            # Just give the game view the same visible models as the battle
            # view for now.
            view.visible_models = self.current_visible_models
            # This long reference is necessary otherwise we get cyclic imports
            controller = Unrealistic_Engine.controllers.game_controller.GameController(self.model, view, self.character_start_position)

            pygame.event.post(pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller, "View": view}))

    def handle_player_start_point(self, pressed_key):
        if pressed_key == pygame.K_UP:
            self.update_target_window(self.test_npc)

    def handle_enemy_start_point(self, pressed_key):
        #if pressed_key == pygame.K_LEFT:
        #if pressed_key == pygame.K_RIGHT:
            
        if pressed_key == pygame.K_DOWN:
            player_position = self.view.get_visible_model_position(self.model.character)
            self.update_target_window(self.model.character)

    def update_target_window(self, new_target_model):
        # Remove outdated target window from visible models
        self.view.remove_model(self.target_window)

        # Update target window with new target model
        self.target_window.current_target = new_target_model

        # Get new target's position
        new_target_position = self.view.get_visible_model_position(new_target_model)

        # Re-add to visible models with new position
        self.view.add_model(self.target_window, BattleView.render_target_window,
                            new_target_position, 2)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
