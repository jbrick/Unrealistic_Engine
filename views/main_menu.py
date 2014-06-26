import pygame
from Unrealistic_Engine.views.menu_view import MenuView
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.map import Map


class MainMenu(MenuView):

    # Leaving space for breadcrumbs
    OFFSET = 50

    PADDING = 10
    FONT_SIZE = 12

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", MainMenu.FONT_SIZE)
        
        line_height = font.size("test")[1] + 1
        
        # Support about 40 characters
        width = 20*MainMenu.FONT_SIZE
        height = 10*line_height+MainMenu.OFFSET
        
        left_corner = Map.MAP_SIZE/2 - width/2
        top_corner  = Map.MAP_SIZE/2 - height/2
        
        # Menu background
        menu_background = pygame.Surface ((width, height), pygame.SRCALPHA)

        #050447
        menu_background.fill((5, 4, 71, 100))
        screen.blit(menu_background, (left_corner, top_corner))

        # Render menu items
        for count in range(0, len(menu.nodes)):
            label = font.render(menu.nodes[count].label, 1, (255, 255, 255))
            screen.blit(label, (
                left_corner + 2*MainMenu.PADDING, top_corner + count*line_height + MainMenu.OFFSET))

            if count == menu.active_node:
                screen.blit(
                    menu.active_icon,
                    (left_corner + MainMenu.PADDING,
                     top_corner + count*line_height + MainMenu.OFFSET + line_height/3))
        
        crumb_position = MainMenu.PADDING
        
        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].active_node].label, 1, (255, 255, 255))
            screen.blit(label, (left_corner + crumb_position, top_corner + MainMenu.PADDING))
            crumb_position += font.size(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].active_node].label) [0]
            
            if crumb >= (len(Menu.breadcrumbs) - 1):
                return
            
            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (left_corner + crumb_position, top_corner + MainMenu.PADDING))
            crumb_position += font.size(" > ")[0]
