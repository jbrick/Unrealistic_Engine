from Unrealistic_Engine.utils.utils import Utils

# Every class that requires input from user should inherit this class.
class Controller():

    # For use with the get_imports function
    MODELS      = 0;
    VIEWS       = 1;
    CONTROLLERS = 2;
    
    def __init__(self, model, view):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def get_imports():
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def qualify_imports(collections):
        models = Utils.dictify(collections [Controller.MODELS])
        views = Utils.dictify(collections [Controller.VIEWS])
        controllers = Utils.dictify(collections [Controller.CONTROLLERS])
        
        models = {k: Utils.qualify_model_name(v) for k, v in models.items ()}
        views = {k: Utils.qualify_view_name(v) for k, v in views.items ()}
        controllers = {k: Utils.qualify_controller_name(v) for k, v in controllers.items ()}

        return (models, views, controllers)


    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def handle_key_press(self, pressed_key):
        raise NotImplementedError("Please Implement this method")
