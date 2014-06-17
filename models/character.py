from Unrealistic_Engine.models.map import Map


class Character:

    SIZE = Map.MAP_SIZE / Map.GRID_SIZE

    def __init__(self, name, image, health, attack):
        self.v_loc = 0
        self.h_loc = 0
        self.name = name
        self.image = image
        self.health = health
        self.attack = attack
