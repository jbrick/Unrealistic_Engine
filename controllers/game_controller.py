import sys
import pygame
import copy

from Unrealistic_Engine.controllers import battle_controller
from Unrealistic_Engine.controllers import menu_controller
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.node_leaf import LeafNode
from Unrealistic_Engine.models.node_menu import MenuNode
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.trigger import Trigger


class GameController(Controller):

    def __init__(self, model, view, character_position):
        self.model = model
        self.view = view
        self.triggers = {}
        self.current_map = model.maps["map3"]
        self.previous_position = None
        self.changed_map = False

        self.__build_triggers()

        # Add Map model
        view.add_model(
            self.current_map, GameView.render_map, Position(0, 0), 1)
        # Add Character model
        view.add_model(
            model.character, GameView.render_character, character_position, 2)

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
        if pressed_key == pygame.K_b:
            view = BattleView()
            
            controller = battle_controller.BattleController(self.model, view, self.view._visible_models,
                                                            self.current_map, position)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))
        if pressed_key == pygame.K_ESCAPE:
            view = MainMenu()

            tmpMenu = Menu()
            tmpChild1 = Menu()
            tmpChild2 = Menu()

            # Create test menus
            tmpChild2.addItem(LeafNode(LeafNode.testFunc, "Child's child 1"))
            tmpChild2.addItem(LeafNode(LeafNode.testFunc, "Child's child 2"))
            tmpChild2.addItem(LeafNode(LeafNode.testFunc, "Child's child 3"))
            tmpChild2.addItem(LeafNode(LeafNode.testFunc, "Child's child 4"))

            tmpChild1.addItem(LeafNode(LeafNode.testFunc, "Child item 1"))
            tmpChild1.addItem(MenuNode(tmpChild2, "Child item 2"))

            tmpMenu.addItem(LeafNode(LeafNode.testFunc, "Test 1"))
            tmpMenu.addItem(LeafNode(LeafNode.testFunc, "Test 2"))
            tmpMenu.addItem(MenuNode(tmpChild1, "Test 3 (I have a submenu)"))

            model = tmpMenu

            controller = menu_controller.MenuController(model, view)

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


