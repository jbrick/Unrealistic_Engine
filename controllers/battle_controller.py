import sys
import pygame
import Unrealistic_Engine.controllers
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.utils import Utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.controllers.controller import Controller


# Currently battle controller just doubles movement speed as a test.
class BattleController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    @staticmethod
    def get_imports():
        models = ["map", "trigger"]
        views = ["battle_view"]
        controllers = ["battle_controller"]
        
        return Controller.qualify_imports((models, views, controllers))

    def handle_key_press(self, pressed_key):
        position = self.view.get_visible_model_position(
            self.model.character)

        if pressed_key == pygame.K_LEFT:
            position.set_x_coord(position.x_coord - 2)
        if pressed_key == pygame.K_RIGHT:
            position.set_x_coord(position.x_coord + 2)
        if pressed_key == pygame.K_UP:
            position.set_y_coord(position.y_coord - 2)
        if pressed_key == pygame.K_DOWN:
            position.set_y_coord(position.y_coord + 2)
        # For testing purposes pressing enter swaps controller / view.
        if pressed_key == pygame.K_RETURN:
            base = Utils.fetch(Utils.qualify_controller_name("game_controller"))
            
            imports = base.GameController.get_imports()
            
            view_module = utils.fetch(imports [base.GameController.VIEWS] ["game_view"])
            
            view = view_module.GameView()
            
            # Just give the game view the same visible models as the battle
            # view for now.
            view.visible_models = self.view.visible_models
            
            controller = base.GameController(self.model, view)

            pygame.event.post(pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller, "View": view}))
            self.view.set_visible_model_position(
                self.model.character, position)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
