import sys
import pygame
from Unrealistic_Engine.controllers.controller import Controller


class GameController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def check_keys(self):
        keys = pygame.key.get_pressed()
        position = self.view.get_visible_model_position(
            self.model.character)

        if keys[pygame.K_LEFT]:
            position.set_x_coord(position.x_coord - 5)         
        if keys[pygame.K_RIGHT]:
            position.set_x_coord(position.x_coord + 5)  
        if keys[pygame.K_UP]:
            position.set_y_coord(position.y_coord - 5)  
        if keys[pygame.K_DOWN]:
            position.set_y_coord(position.y_coord + 5)  

        self.view.set_visible_model_position(
            self.model.character, position)

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            