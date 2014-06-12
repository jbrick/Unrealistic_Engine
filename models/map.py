import sys
import pygame


class Map:
    MAP_SIZE = 640
    GRID_SIZE = 16

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tiles = [[0 for x in xrange(grid_size)]
                      for x in xrange(grid_size)]

    def addOrReplaceTile(self, tile):
        self.tiles[tile.position.x_coord][tile.position.y_coord] = tile

    def get_tile_at_position(self, position):
    	return self.tiles[position.x_coord][position.y_coord]
