import sys, pygame
from Tile import Tile
from Character import Character
from Map import Map

pygame.init()

size = width, height = 640, 640

screen = pygame.display.set_mode(size)

grid_size = 16

map = Map(grid_size)

t1 = pygame.image.load("tile1.bmp")
t2 = pygame.image.load("tile2.bmp")
sprite = pygame.image.load("char.bmp")

character = Character(sprite)

for x in range(0, grid_size):
	for y in range(0, grid_size):
		tile = None
		if x == 5:
			tile = Tile('Floor', t1)
		elif x % 3 == 0:
			if y % 3 == 0:
				tile = Tile('Wall', t2)
			else:
				tile = Tile('Floor', t1)
		else:
			if y % 3 == 2:
				tile = Tile('Wall', t2)
			else:
				tile = Tile('Floor', t1)
		
		map.addOrReplaceTile(tile, x, y)
		#print("Tile of type: %s with Coords vert: %d, Hori: %d\n" % (tile.type, x, y))
map.render(screen, character)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if character.h_loc != 0 and map.tiles[character.v_loc][character.h_loc - 1].type != "Wall":
					character.h_loc -= 1
			if event.key == pygame.K_RIGHT:
				if character.h_loc != (grid_size-1) and map.tiles[character.v_loc][character.h_loc + 1].type != "Wall":
					character.h_loc += 1
			if event.key == pygame.K_UP:
				if character.v_loc != 0 and map.tiles[character.v_loc - 1][character.h_loc].type != "Wall":
					character.v_loc -= 1
			if event.key == pygame.K_DOWN:
				if character.v_loc != (grid_size-1) and map.tiles[character.v_loc + 1][character.h_loc].type != "Wall":
					character.v_loc  += 1
			#map.tiles[character.v_loc][character.h_loc].occupied = 
			print("Character position is: H -> %d, V -> %d" % (character.h_loc, character.v_loc))
			
			
		map.render(screen, character)
		
		pygame.display.flip()