from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.inventory import Inventory
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.mementos.saveable import Saveable
from Unrealistic_Engine.models.mementos.character import CharacterMemento


class Character(Saveable):

    #Directions
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


    SIZE = Map.MAP_SIZE / Map.GRID_SIZE

    def __init__(self, name, image, health, attack):
        self.name = name
        self.image = image
        self.health = health
        self.total_health = health
        self.attack = attack
        self.position = Position(1, 1)
        self.direction = Character.DOWN
        self.inventory = Inventory()

    def create_memento(self):
        return CharacterMemento(self.position, self.health, self.total_health, self.attack)

    def set_memento(self, character_memento):
        self.position = character_memento.position
        self.health = character_memento.health
        self.total_health = character_memento.total_health
        self.attack = character_memento.attack
