import sys
import pygame
from Unrealistic_Engine.controllers import battle_controller
from Unrealistic_Engine.controllers import menu_controller
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.model import Model
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.node import Node
from Unrealistic_Engine.models.node_leaf import LeafNode
from Unrealistic_Engine.models.node_menu import MenuNode
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.trigger import Trigger


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.triggers = {}
        self.build_triggers()

        # Add Map model
        view.add_model(model.maps['Basic'], GameView.render_map, Position(0, 0), 1)
        # Add Character model
        view.add_model(
            model.character, GameView.render_character, Position(0, 0), 2)

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)
        if pressed_key == pygame.K_LEFT:
            position.set_x_coord(position.x_coord - 1)
        if pressed_key == pygame.K_RIGHT:
            position.set_x_coord(position.x_coord + 1)
        if pressed_key == pygame.K_UP:
            position.set_y_coord(position.y_coord - 1)
        if pressed_key == pygame.K_DOWN:
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
            view = MainMenu()
            
            tmpMenu = Menu()
            tmpChild1 = Menu()
            tmpChild2 = Menu()
            
            # Create test menus
            tmpChild2.addItem (LeafNode (LeafNode.testFunc, "Child's child 1"))
            tmpChild2.addItem (LeafNode (LeafNode.testFunc, "Child's child 2"))
            tmpChild2.addItem (LeafNode (LeafNode.testFunc, "Child's child 3"))
            tmpChild2.addItem (LeafNode (LeafNode.testFunc, "Child's child 4"))
            
            tmpChild1.addItem (LeafNode (LeafNode.testFunc, "Child item 1"))
            tmpChild1.addItem (MenuNode (tmpChild2, "Child item 2"))
            
            tmpMenu.addItem (LeafNode (LeafNode.testFunc, "Test 1"))
            tmpMenu.addItem (LeafNode (LeafNode.testFunc, "Test 2"))
            tmpMenu.addItem (MenuNode (tmpChild1, "Test 3 (I have a submenu)"))
            
            model = tmpMenu
            
            controller = menu_controller.MenuController (model, view)

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
            self.handle_trigger(self.triggers[position])

    def build_triggers(self):
        for row in self.model.maps['Basic'].tiles:
            for tile in row:
                if tile != 0 and tile.trigger != None:
                    print "adding trigger to %s" % tile.position
                    self.triggers[tile.position] = tile.trigger

    def handle_trigger(self, trigger):
        if (trigger.action_type == Trigger.CHANGE_MAP):
            # TODO change the map.
            print "Action occurred with data: " + str(trigger.action_data)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
