import pygame
import os

from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.views.battle_view_interface import BattleViewInterface
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.character import Character
from Unrealistic_Engine.views.menu_view import MenuView


class BattleView(BattleViewInterface, MenuView):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0

    TARGET_ICON_OFFSET = -10
    FONT_SIZE = 16
    PADDING = 10
    MENU_HEIGHT = Map.MAP_SIZE / 4
    MENU_WIDTH = Map.MAP_SIZE / 2
    MENU_FONT_SIZE = 16

    # Height of each menu item
    LINE_HEIGHT = 25

    # Leaving space for breadcrumbs
    OFFSET = 50

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):

        character_image = pygame.image.load(os.path.join('Images',
                                                         character.image +
                                                         "_up.png"))
        character_image_scaled = pygame.transform.scale(
            character_image, (Character.SIZE, Character.SIZE))
        screen.blit(character_image_scaled,
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
        font = pygame.font.SysFont("monospace", BattleView.FONT_SIZE)

        base = utils.fetch(utils.qualify_controller_name(
                           "battle_controller"))

        if target_window.battle_state is base.BattleController.TARGET_SELECT:
            # Render the target icon over the new target
            target_image = pygame.image.load(
                os.path.join('Images', "target_icon.png"))
            target_image_scaled = pygame.transform.scale(
                target_image, (10, 10))
            screen.blit(target_image_scaled,
                        position.convert_to_pixels(BattleView.TARGET_ICON_OFFSET))

        # Render enemy stats window
        enemy_background = pygame.Surface((170, 110))
        enemy_background.fill((5, 4, 71, 100))
        enemy_stats_position = Position(11, 2)
        screen.blit(enemy_background, enemy_stats_position.convert_to_pixels(0))

        enemy_name_label = font.render("%s" % target_window.characters['Enemy'].name,
                                       1, (255, 255, 0))
        enemy_health_label = font.render("HP: %d/%d" %
                                         (target_window.characters['Enemy'].health,
                                         target_window.characters['Enemy'].total_health),
                                         1, (255, 255, 255))
        enemy_attack_label = font.render("ATK: %d" % target_window.characters['Enemy'].attack,
                                         1, (255, 255, 255))
        enemy_defense_label = font.render("DEF: %d" % target_window.characters['Enemy'].defense,
                                         1, (255, 255, 255))

        screen.blit(enemy_name_label,
                    enemy_stats_position.convert_with_offset(BattleView.PADDING,
                                                             BattleView.PADDING))
        screen.blit(enemy_health_label,
                    enemy_stats_position.convert_with_offset(BattleView.PADDING,
                                                             BattleView.LINE_HEIGHT +
                                                             BattleView.PADDING))
        screen.blit(enemy_attack_label,
                    enemy_stats_position.convert_with_offset(BattleView.PADDING,
                                                             2 * BattleView.LINE_HEIGHT +
                                                             BattleView.PADDING))
        screen.blit(enemy_defense_label,
                    enemy_stats_position.convert_with_offset(BattleView.PADDING,
                                                             3 * BattleView.LINE_HEIGHT +
                                                             BattleView.PADDING))

        # Render player stats window
        player_background = pygame.Surface((170, 110))
        player_background.fill((5, 4, 71, 100))
        player_stats_position = Position(2, 8)
        screen.blit(player_background, player_stats_position.convert_to_pixels(0))

        player_name_label = font.render("%s" % target_window.characters['Player'].name,
                                        1, (255, 255, 0))
        player_health_label = font.render("HP: %d/%d" %
                                          (target_window.characters['Player'].health,
                                          target_window.characters['Player'].total_health)
                                          , 1, (255, 255, 255))
        player_attack_label = font.render("ATK: %d" % target_window.characters['Player'].attack,
                                          1, (255, 255, 255))
        player_defense_label = font.render("DEF: %d" % target_window.characters['Player'].defense,
                                           1, (255, 255, 255))

        screen.blit(player_name_label,
                    player_stats_position.convert_with_offset(BattleView.PADDING,
                                                              BattleView.PADDING))
        screen.blit(player_health_label,
                    player_stats_position.convert_with_offset(BattleView.PADDING,
                                                              BattleView.LINE_HEIGHT +
                                                              BattleView.PADDING))
        screen.blit(player_attack_label,
                    player_stats_position.convert_with_offset(BattleView.PADDING,
                                                              2 * BattleView.LINE_HEIGHT +
                                                              BattleView.PADDING))
        screen.blit(player_defense_label,
                    player_stats_position.convert_with_offset(BattleView.PADDING,
                                                              3 * BattleView.LINE_HEIGHT +
                                                              BattleView.PADDING))

    @staticmethod
    def render_battle_log(battle_log, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", BattleView.FONT_SIZE)
        large_offset = Map.MAP_SIZE - (Map.MAP_SIZE / 4)

        menu_surface = pygame.Surface((Map.MAP_SIZE/2, Map.MAP_SIZE/4))
        menu_surface.fill((5, 4, 71, 100))
        screen.blit(menu_surface, (Map.MAP_SIZE/2, large_offset))

        num_logs = len(battle_log.battle_log)
        for log_count in range(0, num_logs):
            log_label = font.render(battle_log.battle_log[num_logs - log_count - 1],
                                    1, (255, 255, 255))
            if log_count == 0:
                log_label = font.render(battle_log.battle_log[num_logs - log_count - 1],
                                        1, (255, 255, 0))

            screen.blit(log_label, (Map.MAP_SIZE/2, large_offset + BattleView.PADDING +
                                    (4 - log_count)*BattleView.LINE_HEIGHT))

            if log_count == 4:
                break



