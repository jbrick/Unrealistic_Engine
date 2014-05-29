import sys
import pygame


class Map:
    GRID_SIZE = 16
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tiles = [[0 for x in xrange(grid_size)]
                      for x in xrange(grid_size)]

    def addOrReplaceTile(self, tile, position):
        self.tiles[position.x_coord][position.y_coord] = tile
