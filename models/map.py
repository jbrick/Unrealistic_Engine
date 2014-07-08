class Map:
    MAP_SIZE = 640
    GRID_SIZE = 16

    def __init__(self, grid_size, name):
        self.grid_size = grid_size
        self.name = name
        self.tiles = [[0 for x in xrange(grid_size)]
                      for x in xrange(grid_size)]

    def add_or_replace_tile(self, tile):
        self.tiles[tile.position.x_coord][tile.position.y_coord] = tile

    def get_map_tile(self, pos_x, pos_y):
        if pos_x < 0 or pos_y < 0 or pos_x >Map.GRID_SIZE - 1 or pos_y > Map.GRID_SIZE - 1:
            return None

        return self.tiles[pos_x][pos_y]
