import sys
import pygame
from Unrealistic_Engine.controllers.controller import Controller


class MenuController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def check_keys(self):
        if keys[pygame.K_LEFT] || keys[pygame.K_ESCAPE]:
            # Previous menu
        if keys[pygame.K_RIGHT] || keys[pygame.K_RETURN]:
            # Next menu or select item
        if keys[pygame.K_UP]:
            # Previous item in current menu
        if keys[pygame.K_DOWN]:
            # Next item in current menu

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
