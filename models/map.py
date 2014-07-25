class Map:
    MAP_SIZE = 640
    GRID_SIZE = 16

    def __init__(self, grid_size, name, music):
        self.layers = []
        self.music = music
        self.grid_size = grid_size
        self.name = name
        self.layers.append([[0 for x in xrange(self.grid_size)]for x in xrange(self.grid_size)])
        self.layers.append([[0 for x in xrange(self.grid_size)]for x in xrange(self.grid_size)])

    def add_or_replace_tile(self, layer, tile):
        self.layers[layer][tile.position.x_coord][tile.position.y_coord] = tile

    def get_map_tile(self, pos_x, pos_y, layer):
        if pos_x < 0 or pos_y < 0 or pos_x >Map.GRID_SIZE - 1 or pos_y > Map.GRID_SIZE - 1:
            return None

        return self.layers[layer][pos_x][pos_y]
