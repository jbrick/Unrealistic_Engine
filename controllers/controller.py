import pygame

from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils


# Every class that requires input from user should inherit this class.
class Controller():

    def __init__(self, model, view, previous_controller, previous_view):
        raise NotImplementedError("Please Implement this method")

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        pass

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def handle_key_press(self, pressed_key):
        raise NotImplementedError("Please Implement this method")