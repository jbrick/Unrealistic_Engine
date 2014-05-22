import pygame
from Unrealistic_Engine.views.view import View


class BattleView(View):

    @staticmethod
    def render_character(character, position, screen):
        character_sprite = pygame.image.load(character.image)
        screen.blit(character_sprite, (position.x_coord, position.y_coord))
