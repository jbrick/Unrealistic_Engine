import pygame
from Unrealistic_Engine import event_types


class ControllerFactory():

    @staticmethod
    def build_and_swap_controller(model, controller_name, view_name,
                                  prev_controller, prev_view, *args, **kwargs):
        Controller = ControllerFactory.fetch(
            ControllerFactory.qualify_controller_name(controller_name))
        View = ControllerFactory.fetch(
            ControllerFactory.qualify_view_name(view_name))

        view = View()
        controller = Controller(model, view, prev_controller,
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