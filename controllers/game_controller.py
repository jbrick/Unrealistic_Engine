# import sys
import pygame
import json
from Unrealistic_Engine.utils.utils import Utils
from Unrealistic_Engine.controllers import battle_controller
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.model import Model
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.trigger import Trigger


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.triggers = {}
        self.current_map = model.maps["map3"]

        self.__build_triggers()

        # Add Map model
        view.add_model(
            self.current_map, GameView.render_map, Position(0, 0), 1)
        # Add Character model
        view.add_model(
            model.character, GameView.render_character, Position(0, 0), 2)

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
            view = BattleView()
            # Just give the battle view the same visible models as the
            # game view for now.
            view.visible_models = self.view.visible_models
            controller = battle_controller.BattleController(self.model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))
        if pressed_key == pygame.K_ESCAPE:
            print(Utils.engine)
            
            mview = Utils.fetch("Unrealistic_Engine.views.main_menu")
            menu = Utils.fetch("Unrealistic_Engine.models.menu")
            leaf = Utils.fetch("Unrealistic_Engine.models.node_leaf")
            subm = Utils.fetch("Unrealistic_Engine.models.node_menu")
            mcon = Utils.fetch("Unrealistic_Engine.controllers.menu_controller")
            
            view = mview.MainMenu ()
            
            tmpMenu = menu.Menu()
            tmpChild1 = menu.Menu()
            tmpChild2 = menu.Menu()

            # Create test menus
            tmpChild2.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "Ta"))
            tmpChild2.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "Ta"))
            tmpChild2.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "For"))
            tmpChild2.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "Now"))

            tmpChild1.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "Do Nothing"))
            tmpChild1.addItem(subm.MenuNode
                (tmpChild2, "See More"))

            tmpMenu.addItem(leaf.LeafNode
                (Utils.quit, "Quit"))
            tmpMenu.addItem(leaf.LeafNode
                (leaf.LeafNode.testFunc, "Save"))
            tmpMenu.addItem(subm.MenuNode
                (tmpChild1, "See More"))

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
