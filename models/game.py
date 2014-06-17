from Unrealistic_Engine.models.mementos.saveable import Saveable
from Unrealistic_Engine.models.memento.game import GameMemento


class Game(Saveable):
    def __init__(self, character, maps, current_map):
        self.character = character
        self.maps = maps
        self.current_map = current_map

    def create_memento(self, name):
        character_memento = self.character.create_memento(name)
        return GameMemento(name, self.current_map, character_memento)

    def set_memento(self, game_memento):
        self.current_map = game_memento.current_map
        self.character.set_memento(game_memento.character_memento)