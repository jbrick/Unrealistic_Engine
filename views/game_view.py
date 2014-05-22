import pygame
from Unrealistic_Engine.views.view import View


# Default view for rendering models.
class GameView(View):

    @staticmethod
    def render_character(character, position, screen):
        character_sprite = pygame.image.load(character.image)
        screen.blit(character_sprite, ((position.x_coord * 40) + 10,
                                       (position.y_coord * 40) + 10))

    @staticmethod
    def render_map(game_map, position, screen):
        for x in range(0, game_map.grid_size):
            for y in range(0, game_map.grid_size):
                screen.blit(game_map.tiles[x][y].image, (x * 40, y * 40))
