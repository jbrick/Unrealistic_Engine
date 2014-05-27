import pygame
from Unrealistic_Engine.views.view import View


# Default view for rendering models.
class MenuView(View):

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        # Render caret for currently selected item
        # Render menu items

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        # Render background and breadcrumbs
