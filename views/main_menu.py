import pygame
from Unrealistic_Engine.views.menu_view import MenuView
from Unrealistic_Engine.models.menu import Menu


class MainMenu(MenuView):

    LINE_HEIGHT = 25  # Height of each menu item
    OFFSET = 50       # Leaving space for breadcrumbs
    FONT_SIZE = 20
    PADDING = 10

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        font = pygame.font.SysFont("monospace", MainMenu.FONT_SIZE)
        
        # Clear screen
        screen.fill ((0, 0, 0))
        
        # Render menu items
        for count in range(0, menu.nodeCount):
            label = font.render(menu.nodes [count].label, 1, (255, 255, 255))
            screen.blit(
                label, (2*MainMenu.PADDING, count*MainMenu.LINE_HEIGHT + MainMenu.OFFSET))
            
            if (count == menu.activeNode):
                screen.blit(menu.activeIcon, (MainMenu.PADDING, count*MainMenu.LINE_HEIGHT + MainMenu.OFFSET + MainMenu.PADDING))
        
        crumbPos = MainMenu.PADDING;
        
        # Render breadcrumbs
        for crumb in range(0, len (Menu.breadcrumbs)):
            label = font.render(Menu.breadcrumbs [crumb].nodes [Menu.breadcrumbs [crumb].activeNode].label, 1, (255, 255, 255))
            screen.blit(label, (crumbPos, MainMenu.PADDING))
            crumbPos += font.size(Menu.breadcrumbs [crumb].nodes [Menu.breadcrumbs [crumb].activeNode].label) [0]
            
            if (crumb >= (len(Menu.breadcrumbs) - 1)):
                return
            
            label = font.render(" > ", 1, (255, 0, 0))
            screen.blit(label, (crumbPos, MainMenu.PADDING))
            crumbPos += font.size(" > ") [0]
