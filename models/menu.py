import pygame
import os


class Menu():

    breadcrumbs = []

    """
    Constructor.
    """
    def __init__(self):
        self.nodes = []
        self.active_node = 0;
        self.active_icon = pygame.image.load(os.path.join("Images", "menu_active.png"))

    def get_active_node(self):
        return self.nodes[self.active_node]
