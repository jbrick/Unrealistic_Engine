from Unrealistic_Engine.models.mementos.saveable import Saveable
from Unrealistic_Engine.models.mementos.game import GameMemento


class Game(Saveable):
    def __init__(self, character, maps, enemies, items, current_map):
        self.character = character
        self.maps = maps
        self.enemies = enemies
        self.items = items
        self.current_map = current_map

    def create_memento(self):
        character_memento = self.character.create_memento()
        return GameMemento(self.current_map.name, character_memento)

    def set_memento(self, game_memento):
        self.current_map.name = game_memento.map_name
        self.current_map = self.maps[game_memento.map_name]
        self.character.set_memento(game_memento.character_memento)
