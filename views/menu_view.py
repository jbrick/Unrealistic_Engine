import pygame
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.menu import Menu


class MenuView(View):

    LINE_HEIGHT = 25  # Height of each menu item
    OFFSET = 50       # Leaving space for breadcrumbs

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        pass
    
    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        pass

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", 20)
        
        # Clear screen
        screen.fill ((0, 0, 0))
        
        # Render menu items
        for count in range(0, menu.nodeCount):
            label = font.render(menu.nodes [count].label, 1, (255, 255, 255))
            screen.blit (label, (20, count*MenuView.LINE_HEIGHT + MenuView.OFFSET))
            
            if (count == menu.activeNode):
                screen.blit (menu.activeIcon, (10, count*MenuView.LINE_HEIGHT + MenuView.OFFSET + 10))
        
        crumbPos = 10;
        
        # Render breadcrumbs
        for crumb in range (0, len (menu.stack)):
            label = font.render (menu.stack [crumb].nodes [menu.stack [crumb].activeNode].label, 1, (255, 255, 255))
            screen.blit (label, (crumbPos, 10))
            crumbPos += font.size (menu.stack [crumb].nodes [menu.stack [crumb].activeNode].label) [0]
            
            if (crumb >= (len (menu.stack) - 1)):
                return
            
            label = font.render (" > ", 1, (255, 0, 0))
            screen.blit (label, (crumbPos, 10))
            crumbPos += font.size (" > ") [0]
