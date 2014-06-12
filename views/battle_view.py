import pygame

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.views.battle_view_interface import BattleViewInterface


class BattleView(BattleViewInterface):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        screen.blit(character.image,
                    position.convert_to_pixels(BattleView.CHARACTER_OFFSET))

    @staticmethod
    def render_map(game_tile, screen, *args, **kwargs):
        for x in range(0, Map.GRID_SIZE):
                for y in range(0, Map.GRID_SIZE):
                    position = Position(x, y)
                    screen.blit(game_tile.image,
                                position.convert_to_pixels(0))

    @staticmethod
    def render_enemy(enemy, screen, position, *args, **kwargs):
        screen.blit(enemy.image,
            position.convert_to_pixels(BattleView.CHARACTER_OFFSET))

    #def render_target_indicator():

    #def render_target_window(target_window, screen, *args, **kwargs):

