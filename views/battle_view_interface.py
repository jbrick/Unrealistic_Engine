import pygame
from sets import Set
from Unrealistic_Engine.views.view import View


class BattleViewInterface(View):

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def render_enemy(enemy, screen, position, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")