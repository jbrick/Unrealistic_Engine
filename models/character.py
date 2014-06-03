import sys
from Unrealistic_Engine.models.map import Map


class Character:

    SIZE = Map.MAP_SIZE / (Map.GRID_SIZE)

    def __init__(self, image):
        self.v_loc = 0
        self.h_loc = 0
        self.image = image
