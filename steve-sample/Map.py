import sys, pygame
from Character import Character

class Map:
	def __init__(self, grid_size):
		self.grid_size = grid_size
		self.tiles = [[0 for x in xrange(grid_size)] for x in xrange(grid_size)]

	def addOrReplaceTile(self, tile, v_loc, h_loc):
		 self.tiles[v_loc][h_loc] = tile
		 
	def render(self, screen, character):
		for x in range(0, self.grid_size):
			for y in range(0, self.grid_size):
				screen.blit(self.tiles[x][y].image, (y * 40, x * 40))
		
		screen.blit(character.image, ((character.h_loc * 40) + 10, (character.v_loc * 40) + 10))