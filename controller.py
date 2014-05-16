import model


# Every class that requires input from user should inherit this class.
class Controller():

    # This method gets passed all the pygame events such as a user pressing a
    # key.
    def handle_game_event(self, event):
        raise NotImplementedError("Please Implement this method")