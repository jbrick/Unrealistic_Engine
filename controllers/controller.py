import pygame

from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils import utils


# Every class that requires input from user should inherit this class.
class Controller():

    # For use with the get_imports function
    MODELS = 0
    VIEWS = 1
    CONTROLLERS = 2

    def __init__(self, model, view):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def get_imports():
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def qualify_imports(collections):

        models = utils.dictify(collections[Controller.MODELS])
        views = utils.dictify(collections[Controller.VIEWS])
        controllers = utils.dictify(collections[Controller.CONTROLLERS])
        
        models = {k: utils.qualify_model_name(v) for k, v in models.items()}
        views = {k: utils.qualify_view_name(v) for k, v in views.items()}
        controllers = {k: utils.qualify_controller_name(v) for k, v in controllers.items()}

        return models, views, controllers

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def handle_key_press(self, pressed_key):
        raise NotImplementedError("Please Implement this method")

    def open_main_menu(self, source_view):
        base = utils.fetch(utils.qualify_controller_name(
            "menu_controller"))

        imports = base.MenuController.get_imports()

        view_module = utils.fetch(imports[base.MenuController.VIEWS]["main_menu"])

        model = base.MenuController.build_menu()
        view = view_module.MainMenu()
        controller = base.MenuController(model, view, self, source_view)

        pygame.event.post(
            pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller,
                 "View": view}))
