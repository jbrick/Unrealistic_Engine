import pygame
from Unrealistic_Engine.views.view import View


class MenuView(View):

    @staticmethod
    def render_menu(menu, screen, *args, **kwargs):
        raise NotImplementedError("Please Implement this method")