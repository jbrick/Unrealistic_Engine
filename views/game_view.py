import pygame

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.view import View


# Default view for rendering models.
class GameView(View):

    CHARACTER_OFFSET = 10

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        character_sprite = pygame.image.load(character.image)
        screen.blit(character_sprite,
                    position.convert_to_pixels(GameView.CHARACTER_OFFSET))

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        for x in range(0, game_map.grid_size):
            for y in range(0, game_map.grid_size):
                position = Position(x, y)
                screen.blit(game_map.tiles[x][y].image,
                            position.convert_to_pixels(0))
