import sys
import pygame
from Unrealistic_Engine.controllers.controller import Controller


class MenuController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_key_press(self, pressed_key):
        if (pressed_key == pygame.K_LEFT):
            if (self.model.__nodeStack.nodeCount > 0):
                # Go to previous menu
                model.__activeMenu = model.__nodeStack.pop ();
            else:
                # Do nothing for now. Eventually play a sound or something
        if (pressed_key == pygame.K_RIGHT || pressed_key == pygame.K_RETURN):
            if (isinstance (self.model.nodes [self.model.activeNode], MenuNode)):
                # Traverse into submenu
                self.model.__nodeStack.push (model)
                self.model = self.model.nodes [self.model.activeNode].submenu
            elif (isinstance (self.model.nodes [self.model.activeNode], LeafNode)):
                # Activate action associate with menu item
                self.model.nodes [self.model.activeNode].action ()
        if (pressed_key == pygame.K_UP):
            # Previous item in current menu
            self.model.activeNode--
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode < 0):
                self.model.activeNode = (self.model.nodeCount - 1)
        if (pressed_key == pygame.K_DOWN):
            # Next item in current menu
            self.model.activeNode++
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode >= self.model.nodeCount):
                self.model.activeNode = 0

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
