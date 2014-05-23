class Position():

    TILE_SIZE = 40

    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def set_x_coord(self, x_coord):
        self.x_coord = x_coord

    def set_y_coord(self, y_coord):
        self.y_coord = y_coord

    def convert_to_pixels(self, offset):
        return ((self.x_coord * Position.TILE_SIZE) + offset,
                (self.y_coord * Position.TILE_SIZE) + offset)
