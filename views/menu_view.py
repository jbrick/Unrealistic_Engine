import pygame
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.models.menu import Menu


class MenuView(View):

    LINE_HEIGHT = 25  # Height of each menu item
    OFFSET = 50       # Leaving space for breadcrumbs
    FONT_SIZE = 20
    PADDING = 10

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        pass
    
    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        pass

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", MenuView.FONT_SIZE)
        
        # Clear screen
        screen.fill ((0, 0, 0))
        
        # Render menu items
        for count in range(0, menu.nodeCount):
            label = font.render(menu.nodes [count].label, 1, (255, 255, 255))
            screen.blit(label, (2*MenuView.PADDING, count*MenuView.LINE_HEIGHT + MenuView.OFFSET))
            
            if (count == menu.activeNode):
                screen.blit(menu.activeIcon, (MenuView.PADDING, count*MenuView.LINE_HEIGHT + MenuView.OFFSET + MenuView.PADDING))
        
        crumbPos = MenuView.PADDING;
        
        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes [Menu.breadcrumbs [crumb].activeNode].label, 1, (255, 255, 255))
            screen.blit(label, (crumbPos, MenuView.PADDING))
            crumbPos += font.size(Menu.breadcrumbs [crumb].nodes [Menu.breadcrumbs [crumb].activeNode].label) [0]
            
            if (crumb >= (len(Menu.breadcrumbs) - 1)):
                return
            
            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (crumbPos, MenuView.PADDING))
            crumbPos += font.size(" > ") [0]
