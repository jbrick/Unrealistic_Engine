import pygame
from Unrealistic_Engine.views.view import View


# Default view for rendering models.
class MenuView(View):

    @staticmethod
    def render_character(character, position, screen):
        # Render caret for currently selected item
        # Render menu items
        #   Different function?
