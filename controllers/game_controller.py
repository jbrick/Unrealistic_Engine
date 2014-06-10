# import sys
import pygame
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
        self.current_map = model.maps["map3"]

        self.__build_triggers()

        # Add Map model
        view.add_model(self.current_map, GameView.render_map, Position(0, 0), 1)

        # Add Character model
        view.add_model(
            model.character, GameView.render_character, Position(0, 0), 2)

    @staticmethod
    def getModels():
        models = ["Unrealistic_Engine.models.map",
            "Unrealistic_Engine.models.trigger"]
        
        return models

    @staticmethod
    def getViews():
        views = ["Unrealistic_Engine.views.game_view"]
        
        return views

    @staticmethod
    def getControllers():
        controllers = ["Unrealistic_Engine.controllers.game_controller"]
        
        return controllers

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)
        destination_tile = None
        if pressed_key == pygame.K_LEFT:
            destination_tile = self.get_map_tile(position.x_coord - 1,
                                                 position.y_coord)
            if (position.x_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord - 1)
        if pressed_key == pygame.K_RIGHT:
            destination_tile = self.get_map_tile(position.x_coord + 1,
                                                 position.y_coord)
            if(position.x_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord + 1)
        if pressed_key == pygame.K_UP:
            destination_tile = self.get_map_tile(position.x_coord,
                                                 position.y_coord - 1)
            if(position.y_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord - 1)
        if pressed_key == pygame.K_DOWN:
            destination_tile = self.get_map_tile(position.x_coord,
                                                 position.y_coord + 1)
            if(position.y_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord + 1)
        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_RETURN:
            baseController = Utils.fetch(Utils.qualifyControllerName(
                "battle_controller"))
            
            models = baseController.BattleController.getModels()
            views = baseController.BattleController.getViews()
            controllers = baseController.BattleController.getControllers()
            
            bview = Utils.fetch(views [0])
            bcon = Utils.fetch(controllers [0])
            
            view = bview.BattleView()
            
            # Just give the battle view the same visible models as the
            # game view for now.
            view.visible_models = self.view.visible_models
            controller = bcon.BattleController(self.model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))
        if pressed_key == pygame.K_ESCAPE:
            baseController = Utils.fetch(Utils.qualifyControllerName(
                "menu_controller"))
            
            modelList = baseController.MenuController.getModels()
            viewList = baseController.MenuController.getViews()
            controllerList = baseController.MenuController.getControllers()
            
            mview = Utils.fetch(viewList [0])
            mcon = Utils.fetch(controllerList [0])
            
            view = mview.MainMenu ()
            
            tmpMenu = mcon.MenuController.buildMenu ()

            model = tmpMenu

            controller = mcon.MenuController(model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))

        self.view.set_visible_model_position(
            self.model.character, position)

        # Check if any triggers have been activated.
        print "position is %s" % str(position)
        if position in self.triggers:
            # TODO Handle chance here.
            self.__handle_trigger(self.triggers[position])

    def __change_map(self, map_name):
        self.view.remove_model(self.current_map)
        self.current_map = self.model.maps[map_name]
        self.view.add_model(
            self.current_map, GameView.render_map, Position(0, 0), 1)
        self.triggers = {}
        self.__build_triggers()

    def __build_triggers(self):
        for row in self.current_map.tiles:
            for tile in row:
                if tile != 0 and tile.trigger is not None:
                    print "adding trigger to %s" % tile.position
                    self.triggers[tile.position] = tile.trigger

    def __handle_trigger(self, trigger):
        if (trigger.action_type == Trigger.CHANGE_MAP):
            self.__change_map(trigger.action_data['map_name'])
            print "Action occurred with data: " + str(trigger.action_data)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def get_map_tile(self, pos_x, pos_y):
        max_size = len(self.current_map.tiles)
        if pos_x < 0 or pos_y < 0 or pos_x > max_size - 1 or pos_y > max_size - 1:
            return None

        return self.current_map.tiles[pos_x][pos_y]
