import pygame
import os

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.views.battle_view_interface import BattleViewInterface


class BattleView(BattleViewInterface):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0
    TARGET_ICON_OFFSET = -10
    FONT_SIZE = 20
    PADDING = 10

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

    @staticmethod
    def render_target_window(target_window, screen, position, *args, **kwargs):
        # Render the target icon over the new target
        target_image = pygame.image.load(
            os.path.join('Images', "target_icon.png"))
        target_image_scaled = pygame.transform.scale(
            target_image, (10, 10))
        screen.blit(target_image_scaled, position.convert_to_pixels(BattleView.TARGET_ICON_OFFSET))

        # Update stats window on the right of screen
        font = pygame.font.SysFont("monospace", BattleView.FONT_SIZE)

        name_label = font.render("Name: %s" % target_window.current_target.name, 1, (255, 255, 255))
        health_label = font.render("Health: %d" % target_window.current_target.health, 1, (255, 255, 255))
        attack_label = font.render("Attack: %d" % target_window.current_target.attack, 1, (255, 255, 255))

        screen.blit(name_label, (Map.MAP_SIZE - (Map.MAP_SIZE / 4), (Map.MAP_SIZE / 4)))
        screen.blit(health_label, (Map.MAP_SIZE - (Map.MAP_SIZE / 4), (Map.MAP_SIZE / 4) + 20))
        screen.blit(attack_label, (Map.MAP_SIZE - (Map.MAP_SIZE / 4), (Map.MAP_SIZE / 4) + 40))



