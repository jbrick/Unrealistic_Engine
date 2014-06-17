import sys
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.mementos.saveable import Saveable
from Unrealistic_Engine.models.mementos.character import CharacterMemento


class Character(Saveable):

    SIZE = Map.MAP_SIZE / Map.GRID_SIZE

    def __init__(self, image):
        self.position = Position (0, 0)
        self.image = image

    def create_memento(self):
        return CharacterMemento(self.position)

    def set_memento(self, character_memento):
        self.position = character_memento.position
