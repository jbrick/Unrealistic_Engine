import pygame
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.menu import Menu


class MenuView(View):

    OFFSET = 50
    PADDING = 10
    FONT_SIZE = 12
    WIDTH = 200
    HEIGHT = 200

    @classmethod
    def render_menu(cls, menu, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", cls.FONT_SIZE)

        line_height = font.size("test")[1] + 1

        # Menu background
        menu_background = pygame.Surface ((cls.WIDTH, cls.HEIGHT), pygame.SRCALPHA)

        #050447
        menu_background.fill((5, 4, 71, 100))
        screen.blit(menu_background, (position.x_coord, position.y_coord))

        # Render menu items
        for count in range(0, len(menu.nodes)):
            label = font.render(menu.nodes[count].label, 1, (255, 255, 255))
            screen.blit(label, (
                position.x_coord + 2*cls.PADDING, position.y_coord +
                count*line_height + cls.OFFSET))

            if count == menu.get_active_node_index():
                screen.blit(
                    menu.active_icon,
                    (position.x_coord + cls.PADDING,
                     position.y_coord + count*line_height + cls.OFFSET +
                     line_height/3))

        crumb_position = cls.PADDING

        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].get_active_node_index()].label, 1,
                                (255, 255, 255))
            screen.blit(label, (position.x_coord + crumb_position, position.y_coord +
                                cls.PADDING))
            crumb_position += font.size(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].get_active_node_index()].label) [0]

            if crumb >= (len(Menu.breadcrumbs) - 1):
                return

            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (position.x_coord + crumb_position, position.y_coord +
                                cls.PADDING))
            crumb_position += font.size(" > ")[0]