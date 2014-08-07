import pygame

from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.database import Database


# Every class that requires input from user should inherit this class.
class Controller():

    @staticmethod
    def build_and_swap_controller(model, controller_name, view_name,
                                  prev_controller, prev_view, *args, **kwargs):

        if model is None:
            model = Database().load_application()

        controller_module = Controller.fetch(
            Controller.qualify_controller_name(controller_name))
        view_module = Controller.fetch(
            Controller.qualify_view_name(view_name))

        view = view_module()
        controller = controller_module(model, view, prev_controller,
                                       prev_view, *args, **kwargs)

        pygame.event.post(
            pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller,
                 "View": view}))


    @staticmethod
    def fetch(path):
        # path is a tuple (module, class)
        module = __import__(path[0], fromlist=[path[1]])

        cls = getattr(module, path[1])

        return cls


    @staticmethod
    def qualify_view_name(name):
        return ("Unrealistic_Engine.views." + name, name.title(
        ).replace('_', ''))

    @staticmethod
    def qualify_controller_name(name):
        return ("Unrealistic_Engine.controllers." + name, name.title(
        ).replace('_', ''))

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