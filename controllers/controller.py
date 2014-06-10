# Every class that requires input from user should inherit this class.
class Controller():

    def __init__(self, model, view):
        raise NotImplementedError("Please Implement this method")

    """
    Retrieves the list of models associated with this controller.
    """
    @staticmethod
    def getModels():
        raise NotImplementedError("Please Implement this method")

    """
    Retrieves the list of views associated with this controller
    """
    @staticmethod
    def getViews():
        raise NotImplementedError("Please Implement this method")

    """
    Retrieves the list of controllers associated with this controller
    """
    @staticmethod
    def getControllers():
        raise NotImplementedError("Please Implement this method")

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")

    # Called from main game loop. Allows controller to check state of all
    # pressed keys.
    def handle_key_press(self, pressed_key):
        raise NotImplementedError("Please Implement this method")
