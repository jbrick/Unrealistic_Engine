import pygame
import os
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.menu import Menu


class MenuView(View):

    MENU_OFFSET = 50
    MENU_PADDING = 10
    MENU_FONT_SIZE = 12
    MENU_WIDTH = 200
    MENU_HEIGHT = 200
    MENU_IMAGE = None
    MENU_FONT_COLOR = (255, 255, 255)

    @classmethod
    def render_menu(cls, menu, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", cls.MENU_FONT_SIZE)

        line_height = font.size("test")[1] + 1

        if cls.MENU_IMAGE is None:
            # Menu background
            menu_background = pygame.Surface ((cls.MENU_WIDTH, cls.MENU_HEIGHT))

            #050447
            menu_background.fill((5, 4, 71, 100))
        else:
            title_image = pygame.image.load(os.path.join('Images',
                                                         cls.MENU_IMAGE))
            menu_background = pygame.transform.scale(
                title_image, (cls.MENU_WIDTH, cls.MENU_HEIGHT))


        screen.blit(menu_background, (position.x_coord, position.y_coord))

        # Render menu items
        for count in range(0, len(menu.nodes)):
            label = font.render(menu.nodes[count].label, 1, cls.MENU_FONT_COLOR)
            screen.blit(label, (
                position.x_coord + 2*cls.MENU_PADDING, position.y_coord +
                count*line_height + cls.MENU_OFFSET))

            if count == menu.get_active_node_index():
                screen.blit(
                    menu.active_icon,
                    (position.x_coord + cls.MENU_PADDING,
                     position.y_coord + count*line_height + cls.MENU_OFFSET +
                     line_height/3))

        crumb_position = cls.MENU_PADDING

        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].get_active_node_index()].label, 1,
                                cls.MENU_FONT_COLOR)
            screen.blit(label, (position.x_coord + crumb_position, position.y_coord +
                                cls.MENU_OFFSET - 50))
            crumb_position += font.size(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].get_active_node_index()].label) [0]

            if crumb >= (len(Menu.breadcrumbs) - 1):
                return

            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (position.x_coord + crumb_position, position.y_coord +
                                cls.MENU_OFFSET - 50))
            crumb_position += font.size(" > ")[0]