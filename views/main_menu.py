import pygame
from Unrealistic_Engine.views.menu_view import MenuView
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.map import Map


class MainMenu(MenuView):

    OFFSET = 50       # Leaving space for breadcrumbs
    PADDING = 10
    FONT_SIZE = 12

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", MainMenu.FONT_SIZE)
        
        line_height = font.size("test") [1] + 1
        
        # Support about 40 characters
        width = 20*MainMenu.FONT_SIZE
        height = 10*line_height+MainMenu.OFFSET
        
        left_corner = Map.MAP_SIZE/2 - width/2
        top_corner  = Map.MAP_SIZE/2 - height/2
        
        # Menu background
        menu_background = pygame.Surface ((width, height), pygame.SRCALPHA)
        menu_background.fill((5, 4, 71, 100)) #050447
        screen.blit (menu_background, (left_corner, top_corner))

        # Render menu items
        for count in range(0, menu.nodeCount):
            label = font.render(menu.nodes [count].label, 1, (255, 255, 255))
            screen.blit(label, (left_corner + 2*MainMenu.PADDING, top_corner + count*line_height +
                    MainMenu.OFFSET))

            if (count == menu.activeNode):
                screen.blit(menu.activeIcon, (left_corner + MainMenu.PADDING, top_corner + 
                    count*line_height + MainMenu.OFFSET + line_height/3))
        
        crumbPos = MainMenu.PADDING;
        
        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].activeNode].label, 1, (255, 255, 255))
            screen.blit(label, (left_corner + crumbPos, top_corner + MainMenu.PADDING))
            crumbPos += font.size(Menu.breadcrumbs [crumb].nodes
                [Menu.breadcrumbs [crumb].activeNode].label) [0]
            
            if (crumb >= (len(Menu.breadcrumbs) - 1)):
                return
            
            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (left_corner + crumbPos, top_corner + MainMenu.PADDING))
            crumbPos += font.size(" > ") [0]
