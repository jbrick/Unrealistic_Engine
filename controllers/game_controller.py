import pygame
import copy
import json
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.utils import Utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.trigger import Trigger
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.controllers.controller import Controller


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.triggers = {}
        self.current_map = model.maps["tower_floor1"]
        self.previous_position = None
        self.changed_map = False

        self.__build_triggers()

        # Add Map model
        view.add_model(self.current_map, GameView.render_map, Position(0, 0), 1)
        
        # Add Character model
        view.add_model(
            model.character, GameView.render_character, Position(1, 1), 2)

    @staticmethod
    def get_imports():
        models = ["map", "trigger"]
        views = ["game_view"]
        controllers = ["game_controller"]
        
        return Controller.qualify_imports((models, views, controllers))

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)
        destination_tile = None
        if pressed_key == pygame.K_LEFT:
            destination_tile = self.current_map.get_map_tile(
                position.x_coord - 1,position.y_coord)
            if (position.x_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord - 1)
        if pressed_key == pygame.K_RIGHT:
            destination_tile = self.current_map.get_map_tile(
                position.x_coord + 1,position.y_coord)
            if(position.x_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord + 1)
        if pressed_key == pygame.K_UP:
            destination_tile = self.current_map.get_map_tile(position.x_coord,
                                                 position.y_coord - 1)
            if(position.y_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord - 1)
        if pressed_key == pygame.K_DOWN:
            destination_tile = self.current_map.get_map_tile(position.x_coord,
                                                 position.y_coord + 1)
            if(position.y_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord + 1)
        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_RETURN:
            base = Utils.fetch(Utils.qualify_controller_name(
                "battle_controller"))
            
            imports = base.BattleController.get_imports()
            
            view_module = Utils.fetch(imports [base.BattleController.VIEWS] ["battle_view"])
            
            view = view_module.BattleView()
            
            # Just give the battle view the same visible models as the
            # game view for now.
            view.visible_models = self.view.visible_models
            controller = base.BattleController(self.model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))
        if pressed_key == pygame.K_ESCAPE:
            base = Utils.fetch(Utils.qualify_controller_name(
                "menu_controller"))
            
            imports = base.MenuController.get_imports()
            
            view_module = Utils.fetch(imports [base.MenuController.VIEWS] ["main_menu"])
            
            model = base.MenuController.build_menu ()
            view = view_module.MainMenu ()
            controller = base.MenuController(model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))

        self.view.set_visible_model_position(self.model.character, position)

        # Check if any triggers have been activated.
        print "previous position is %s" % str(self.previous_position)
        print "position is %s" % str(position)

        if position in self.triggers:
            # TODO Handle chance here.
            self.__handle_trigger(self.triggers[position], position, False)
        if self.previous_position in self.triggers:
            # TODO Handle chance here.
            self.__handle_trigger(self.triggers[self.previous_position], self.previous_position, True)

        self.previous_position = copy.copy(position)
        if self.changed_map:
            # If we changed maps we need to reset our previous position such that we don't fire the
            # trigger twice.
            self.previous_position = None
            self.changed_map = False

    def __change_map(self, map_name):
        self.changed_map = True
        self.view.remove_model(self.current_map)
        self.current_map = self.model.maps[map_name]
        self.view.add_model(
            self.current_map, GameView.render_map, Position(0, 0), 1)
        self.triggers = {}
        self.previous_position = None
        self.__build_triggers()

    def __build_triggers(self):
        for row in self.current_map.tiles:
            for tile in row:
                if tile != 0 and tile.trigger is not None:
                    self.triggers[tile.position] = tile.trigger

    def __handle_trigger(self, trigger, position, is_previous):

        # We support triggers being fired when entering or leaving a tile.
        valid_previous_trigger = trigger.triggered_on == "exit" and is_previous
        valid_current_trigger = trigger.triggered_on == "enter" and not is_previous

        if valid_current_trigger or valid_previous_trigger:
            if trigger.action_type == Trigger.CHANGE_MAP:
                self.__change_map(trigger.action_data['map_name'])
                position = Position(
                    trigger.action_data['character_x'],
                    trigger.action_data['character_y'])

                self.view.set_visible_model_position(self.model.character, position)


            print "Action occurred with data: " + str(trigger.action_data)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


