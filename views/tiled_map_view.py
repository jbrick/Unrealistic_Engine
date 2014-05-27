import pygame
from Unrealistic_Engine.views.view import View


class TiledMapView(View):

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")
