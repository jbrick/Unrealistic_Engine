import sys
import pygame
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.menu_view import MenuView
from Unrealistic_Engine.models.node import Node
from Unrealistic_Engine.models.node_leaf import LeafNode
from Unrealistic_Engine.models.node_menu import MenuNode
from Unrealistic_Engine.models.menu import Menu


class MenuController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        view.add_model(self.model, MenuView.render_menu, 0, View.BACKGROUND)
        MenuController.activeMenu = model

    def handle_key_press(self, pressed_key):
        if (pressed_key == pygame.K_LEFT):
            if (len(Menu.breadcrumbs) > 0):
                # Go to previous menu
                self.view.remove_model(self.model)
                self.model = Menu.breadcrumbs.pop();
                self.view.add_model(self.model, MenuView.render_menu, 0, View.BACKGROUND)
        if (pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN):
            if (isinstance(self.model.nodes [self.model.activeNode], MenuNode)):
                # Traverse into submenu
                Menu.breadcrumbs.append(self.model)
                self.view.remove_model(self.model)
                self.model = self.model.nodes [self.model.activeNode].submenu
                self.view.add_model(self.model, MenuView.render_menu, 0, View.BACKGROUND)
            elif (isinstance(self.model.nodes [self.model.activeNode], LeafNode)):
                # Activate action associate with menu item
                self.model.nodes [self.model.activeNode].action()
        if (pressed_key == pygame.K_UP):
            # Previous item in current menu
            self.model.activeNode -= 1
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode < 0):
                self.model.activeNode = (self.model.nodeCount - 1)
        if (pressed_key == pygame.K_DOWN):
            # Next item in current menu
            self.model.activeNode += 1
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode >= self.model.nodeCount):
                self.model.activeNode = 0
            
    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
