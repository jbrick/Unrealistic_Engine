import pygame

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.map_view import MapView


# Default view for rendering models
class GameView(MapView):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        screen.blit(character.image,
                    position.convert_to_pixels(GameView.CHARACTER_OFFSET))

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        for x in range(0, game_map.grid_size):
            for y in range(0, game_map.grid_size):
                position = Position(x, y)
                if game_map.tiles[x][y] != 0:
                    screen.blit(game_map.tiles[x][y].image,
                                position.convert_to_pixels(0))
