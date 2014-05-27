import sys
import pygame
import Unrealistic_Engine.controllers
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.position import Position


# Currently battle controller just doubles movement speed as a test.
class BattleController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

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
            view = GameView()
            # Just give the game view the same visible models as the battle
            # view for now.
            view.visible_models = self.view.visible_models
            # This long reference is neccessary otherwise we get cyclic imports
            controller = Unrealistic_Engine.controllers.game_controller.GameController(self.model, view)

            pygame.event.post(pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller, "View": view}))
            self.view.set_visible_model_position(
                self.model.character, position)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
