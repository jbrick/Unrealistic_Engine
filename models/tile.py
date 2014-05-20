import sys


class Tile:
    def __init__(self, type, image):
        self.type = type
        self.occupied = False
        self.image = image