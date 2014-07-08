import sys


class NPC:

    def __init__(self, name, health, image, alive):
        self.health = health
        self.name = name
        self.image = image
        self.alive = alive
        self.h_loc = 0
        self.v_loc = 0