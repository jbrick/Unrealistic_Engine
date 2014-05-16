import model


# Every class that requires input from user should inherit this class.
class Controller():

    def __init__ (self, model, view):
        raise NotImplementedError("Please Implement this method")

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def check_keys(self):
        raise NotImplementedError("Please Implement this method")