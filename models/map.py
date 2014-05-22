import sys
import pygame


class Map:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tiles = [[0 for x in xrange(grid_size)]
                      for x in xrange(grid_size)]

    def addOrReplaceTile(self, tile, h_loc, v_loc):
        self.tiles[h_loc][v_loc] = tile
