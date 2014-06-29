import pygame
import copy
import sys
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.dialog import Dialog
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.trigger import Trigger
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.controllers.controller import Controller


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.triggers = {}

        self.previous_position = None
        self.changed_map = False

        self._build_triggers()

        # Add Map model
        view.add_model(model.current_map, GameView.render_map, Position(0, 0), GameView.BACKGROUND)
        
        # Add Character model
        view.add_model(
            model.character,
            GameView.render_character,
            model.character.position,
            GameView.FOREGROUND)

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
            destination_tile = self.model.current_map.get_map_tile(
                position.x_coord - 1, position.y_coord)
            if (position.x_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord - 1)
        if pressed_key == pygame.K_RIGHT:
            destination_tile = self.model.current_map.get_map_tile(
                position.x_coord + 1, position.y_coord)
            if(position.x_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_x_coord(position.x_coord + 1)
        if pressed_key == pygame.K_UP:
            destination_tile = self.model.current_map.get_map_tile(
                position.x_coord, position.y_coord - 1)
            if(position.y_coord - 1) >= 0 and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord - 1)
        if pressed_key == pygame.K_DOWN:
            destination_tile = self.model.current_map.get_map_tile(
                position.x_coord, position.y_coord + 1)
            if(position.y_coord + 1) < Map.GRID_SIZE and destination_tile.walkable == 1:
                position.set_y_coord(position.y_coord + 1)
        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_RETURN:
            base = utils.fetch(utils.qualify_controller_name(
                "battle_controller"))
            
            imports = base.BattleController.get_imports()
            
            view_module = utils.fetch(imports [base.BattleController.VIEWS] ["battle_view"])
            
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
            base = utils.fetch(utils.qualify_controller_name(
                "menu_controller"))
            
            imports = base.MenuController.get_imports()
            
            view_module = utils.fetch(imports [base.MenuController.VIEWS] ["main_menu"])

            view = view_module.MainMenu ()
            controller = base.MenuController(self.model, view)

            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": controller,
                     "View": view}))

        self.view.set_visible_model_position(self.model.character, position)
        self.model.character.position = position

        # Check if any triggers have been activated.
        if position in self.triggers:
            # TODO Handle chance here.
            self._handle_trigger(self.triggers[position], position, False)
        if self.previous_position in self.triggers:
            # TODO Handle chance here.
            self._handle_trigger(self.triggers[self.previous_position], self.previous_position, True)

        self.previous_position = copy.copy(position)
        if self.changed_map:
            # If we changed maps we need to reset our previous position such that we don't fire the
            # trigger twice.
            self.previous_position = None
            self.changed_map = False

    def _change_map(self, map_name):
        self.changed_map = True
        self.view.remove_model(self.model.current_map)
        self.model.current_map = self.model.maps[map_name]
        self.view.add_model(
            self.model.current_map, GameView.render_map, Position(0, 0), GameView.BACKGROUND)
        self.triggers = {}
        self.previous_position = None
        self._build_triggers()

    def _build_triggers(self):
        for row in self.model.current_map.tiles:
            for tile in row:
                if tile != 0 and tile.trigger is not None:
                    self.triggers[tile.position] = tile.trigger

    def _handle_trigger(self, trigger, position, is_previous):
        # We support triggers being fired when entering or leaving a tile.
        valid_previous_trigger = trigger.triggered_on == "exit" and is_previous
        valid_current_trigger = trigger.triggered_on == "enter" and not is_previous

        if valid_current_trigger or valid_previous_trigger:
            if trigger.action_type == Trigger.CHANGE_MAP:
                self._change_map(trigger.action_data['map_name'])
                position = Position(
                    trigger.action_data['character_x'],
                    trigger.action_data['character_y'])

                self.view.set_visible_model_position(self.model.character, position)
            if trigger.action_type == Trigger.SHOW_DIALOG:
                new_dialog = Dialog(
                    Position(trigger.action_data['dialog_x'], trigger.action_data['dialog_y']),
                    trigger.action_data['dialog_text'],
                    trigger.action_data['timed'],
                    trigger.action_data['timeout'])
                self.view.add_model(
                    new_dialog, GameView.render_dialog, new_dialog.location, GameView.OVERLAY)

            print "Action occurred with data: " + str(trigger.action_data)

    def handle_game_event(self, event):
        if event.type == event_types.KILL_DIALOG:
            self.view.remove_model(event.Dialog)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
