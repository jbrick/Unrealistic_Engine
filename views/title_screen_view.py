import pygame
from Unrealistic_Engine.views.menu_view import MenuView
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.map import Map


class TitleScreenView(MenuView):

    MENU_OFFSET = Map.MAP_SIZE - 120
    MENU_PADDING = 10
    MENU_FONT_SIZE = 36
    MENU_WIDTH = Map.MAP_SIZE
    MENU_HEIGHT = Map.MAP_SIZE
    #TODO don't hardcode the title screen image
    MENU_IMAGE = "castle.jpg"
    MENU_FONT_COLOR = (255, 255, 255)

    @classmethod
    def after_visible_models_rendered(cls, screen):
        # Render title
        font = pygame.font.SysFont("monospace", cls.MENU_FONT_SIZE)
        #TODO don't hardcode the game title
        label = font.render("Castle Doom", 1, cls.MENU_FONT_COLOR)
        screen.blit(label, (25, 25))