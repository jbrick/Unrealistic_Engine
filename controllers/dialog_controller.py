import pygame

from Unrealistic_Engine.controllers.controller_factory import ControllerFactory
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.views.dialog_view import DialogView

class DialogController(Controller):
    
    def __init__(self, model, view, *args, **kwargs):
        self.active_dialog = model
        self.view = view
        self.view.add_model(model, DialogView.render_dialog, model.location,
                            GameView.OVERLAY)

    def handle_key_press(self, pressed_key):
        if pressed_key == pygame.K_RETURN:
            Controller.build_and_swap_controller(None, "game_controller",
                                                 "game_view", self, self.view)
