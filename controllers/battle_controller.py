import sys
import os
import pygame
import Unrealistic_Engine.controllers
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.character import Character
from Unrealistic_Engine.models.npc import NPC
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.position import Position


class BattleController(Controller):

    ACTION = "Action Select"
    TARGET = "Target Select"
    ENEMY = "Enemy Turn"

    def __init__(self, model, view, current_visible_models, current_map, character_start_position):
        self.model = model
        self.view = view
        self.state = self.TARGET
        self.current_visible_models = current_visible_models
        self.current_map = current_map
        self.character_start_position = character_start_position

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
        test_npc = NPC("Boss1", 100, npc_image_scaled, 1)
        self.view.add_model(
            test_npc, BattleView.render_enemy, Position(Map.GRID_SIZE/2, 2), 2)

        self.active_enemies = set()
        self.active_enemies.add(test_npc)

        self.current_target = active_enemies(0)

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)

        if state is TARGET:
            if type(self.target) is Character:
                handle_character_start_point(pressed_key)
            else:
                handle_enemy_start_point(pressed_key)


        #elif state is ACTION:

        

        #elif state is ENEMY:


        #if pressed_key == pygame.K_LEFT:

        #if pressed_key == pygame.K_RIGHT:

        #if pressed_key == pygame.K_UP:

        #if pressed_key == pygame.K_DOWN:

        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_RETURN:
            view = GameView()
            # Just give the game view the same visible models as the battle
            # view for now.
            view.visible_models = self.current_visible_models
            # This long reference is neccessary otherwise we get cyclic imports
            controller = Unrealistic_Engine.controllers.game_controller.GameController(self.model, view, self.character_start_position)

            pygame.event.post(pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller, "View": view}))

    def handle_character_start_point(pressed_key):
        if pressed_key == pygame.K_UP:
            self.current_target = self.active_enemies(0)

    def handle_enemy_start_point(pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.current_target = self.active_enemies()
        if pressed_key == pygame.K_RIGHT:
            
        if pressed_key == pygame.K_DOWN:
            self.current_target = self.model.character

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
