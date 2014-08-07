import os
import pygame

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.map_view import MapView
from Unrealistic_Engine.views.dialog_view import DialogView
from Unrealistic_Engine.models.character import Character



# Default view for rendering models
class GameView(MapView, DialogView):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        qualifier = "_" + character.direction + ".png"

        character_image = pygame.image.load(os.path.join('Images',
                                                         character.image +
                                                         qualifier))
        character_image_scaled = pygame.transform.scale(
            character_image, (Character.SIZE, Character.SIZE))
        screen.blit(character_image_scaled,
                    position.convert_to_pixels(GameView.CHARACTER_OFFSET))

    @staticmethod
    def render_map(map, screen, *args, **kwargs):
        #render layer 1
        for x in range(0, map.grid_size):
            for y in range(0, map.grid_size):
                position = Position(x, y)
                if map.layers[0][x][y] != 0:
                    screen.blit(map.layers[0][x][y].image,
                                position.convert_to_pixels(0))

        #render layer 2
        for x in range(0, map.grid_size):
            for y in range(0, map.grid_size):
                position = Position(x, y)
                if map.layers[1][x][y] != 0:
                    screen.blit(map.layers[1][x][y].image,
                                position.convert_to_pixels(0))
