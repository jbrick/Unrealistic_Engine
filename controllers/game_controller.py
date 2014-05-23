import sys
import pygame
from Unrealistic_Engine.controllers import battle_controller
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.battle_view import BattleView
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.model import Model
from Unrealistic_Engine.utils.position import Position


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def check_keys(self):
        keys = pygame.key.get_pressed()
        position = self.view.get_visible_model_position(
            self.model.character)

        if keys[pygame.K_LEFT]:
            position.set_x_coord(position.x_coord - 1)
        if keys[pygame.K_RIGHT]:
            position.set_x_coord(position.x_coord + 1)
        if keys[pygame.K_UP]:
            position.set_y_coord(position.y_coord - 1)
        if keys[pygame.K_DOWN]:
            position.set_y_coord(position.y_coord + 1)
        # For testing purposes pressing enter swaps controller / view.
        if keys[pygame.K_RETURN]:
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

        self.view.set_visible_model_position(
            self.model.character, position)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
