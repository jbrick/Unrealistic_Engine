import sys
from Unrealistic_Engine.models.map import Map


class Tile:

    SIZE = Map.MAP_SIZE / Map.GRID_SIZE

    def __init__(self, type, image, position, trigger):
        self.type = type
        self.occupied = False
        self.image = image
        self.position = position
        self.trigger = trigger
