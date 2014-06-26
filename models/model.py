class Model():

    def load_application(self):
        """
        The model must implement this to load all game data into memory.

        :raise NotImplementedError:
        """
        raise NotImplementedError("Please Implement this method")


    def save_game(self, game_memento):
        """
        The model must implement this to save a game's state such as character health position etc.

        :raise NotImplementedError:
        """
        raise NotImplementedError("Please Implement this method")

    def get_saved_games(self):
        """
        Must be implemented by the model to return all saved game names from the data store

        """

    def load_saved_game(self, memento_name):
        """
         The model must implement this to load a saved_game of the specified name.

        :raise NotImplementedError:
        """
        raise NotImplementedError("Please Implement this method")
