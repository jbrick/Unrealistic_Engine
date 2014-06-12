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

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def handle_key_press(self, pressed_key):
        raise NotImplementedError("Please Implement this method")
