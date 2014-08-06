import pygame

from Unrealistic_Engine import event_types
from Unrealistic_Engine.controllers.controller import Controller

class DialogController(Controller):
    
    def __init__(self, model, view, *args, **kwargs):
        self.active_dialog = model
        self.view = view

    def handle_key_press(self, pressed_key):
        if pressed_key == pygame.K_SPACE:
            pygame.event.post(
                pygame.event.Event(
                    event_types.UPDATE_GAME_STATE,
                    {"Controller": self.active_dialog.scene,
                     "View": self.view}))

            pygame.event.post(
                pygame.event.Event(
                    event_types.KILL_DIALOG,
                    {"Dialog": self.active_dialog}))
