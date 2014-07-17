from Unrealistic_Engine.models.tile import Tile

class Position():

    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __eq__(self, othr):
        return ((self.x_coord, self.y_coord) == (othr.x_coord, othr.y_coord))

    def __hash__(self):
        return hash((self.x_coord, self.y_coord))

    def __str__(self):
        return "x: %d, y: %d" % (self.x_coord, self.y_coord)

    def set_x_coord(self, x_coord):
        self.x_coord = x_coord

    def set_y_coord(self, y_coord):
        self.y_coord = y_coord

    def convert_to_pixels(self, offset):
        return ((self.x_coord * Tile.SIZE) + offset,
                (self.y_coord * Tile.SIZE) + offset)

    def convert_with_offset(self, x_offset, y_offset):
        return ((self.x_coord * Tile.SIZE + x_offset),
                (self.y_coord * Tile.SIZE) + y_offset)