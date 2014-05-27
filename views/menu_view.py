import pygame
from Unrealistic_Engine.views.view import View


# Default view for rendering models.
class MenuView(View):

    LINE_HEIGHT = 25  # Height of each menu item
    OFFSET = 50       # Leaving space for breadcrumbs

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        pass
    
    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        pass

    # Render menu items
    # Render caret for currently selected item
    # Render background and breadcrumbs
    def render_menu(menu, screen, *args, **kwargs):
        # Needs to be run after pygame initalizes, so it should be here rather than above
        font = pygame.font.SysFont("monospace", 20)
        
        # Render menu items
        for count in range(0, menu.nodeCount):
            label = font.render(menu.nodes [count].label, 1, (255, 255, 255))
            screen.blit (label, (50, count*LINE_HEIGHT + OFFSET))
            
            if (count == menu.activeNode):
                screen.blit (menu.activeIcon, (10, count*LINE_HEIGHT + OFFSET + 10))
        
        crumbPos = 10;
        
        # Render breadcrumbs
        for crumb in range (0, (len (menu.__nodeStack) - 1)):
            label = font.render (menu.__nodeStack [crumb].label, 1, (255, 255, 255))
            screen.blit (label, (crumbPos, 10))
            crumbPos += font.size (label) [0]
            
            if (crumb >= len (menu.__nodeStack)):
                return
            
            label = font.render (" > ", 1, (255, 0, 0))
            screen.blit (label, (crumbPos, 10))
            crumbPos += font.size (label) [0]
            
