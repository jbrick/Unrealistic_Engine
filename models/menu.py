import pygame
import os

from Unrealistic_Engine.views.view import View

class Menu():

    breadcrumbs = []

    """
    Constructor.
    """
    def __init__(self, view, render_function, on_node_activated, position):
        self.view = view
        self.nodes = []
        self.on_node_activated = on_node_activated
        self._active_node_index = 0;
        self.active_icon = pygame.image.load(os.path.join("Images", "menu_active.png"))
        self.render_function = render_function
        self.position = position
        self.view.add_model(self, self.render_function, position,
                        View.BACKGROUND)

    def get_active_node(self):
        return self.nodes[self._active_node_index]

    def inc_active_node(self):
        self._active_node_index += 1
        if self._active_node_index >= len(self.nodes):
            self._active_node_index = 0

    def get_active_node_index(self):
        return self._active_node_index

    def dec_active_node(self):
        self._active_node_index -= 1
        if self._active_node_index < 0:
            self._active_node_index = len(self.nodes) - 1

    def go_to_previous_menu(self):
        self.view.remove_model(self)
        self = Menu.breadcrumbs.pop()
        self.view.add_model(self, self.render_function, self.position,
                            View.BACKGROUND)
        return self

    def activate_node(self):
        self.on_node_activated(self.get_active_node())
        if not self.get_active_node().is_leaf_node():
            return self.go_to_submenu()
        return self

    def go_to_submenu(self):
        Menu.breadcrumbs.append(self)
        self.view.remove_model(self)
        self = self.get_active_node().submenu
        self.view.add_model(self, self.render_function, self.position,
                            View.BACKGROUND)
        return self