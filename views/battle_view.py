import pygame
from Unrealistic_Engine.views.map_view import MapView


class BattleView(MapView):

    @staticmethod
    def render_character(character, position, screen):
        screen.blit(character_sprite, (position.x_coord, position.y_coord))
