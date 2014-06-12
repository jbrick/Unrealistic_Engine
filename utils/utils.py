import pygame

class Utils:

    engine = __import__("Unrealistic_Engine")

    @staticmethod
    def fetch(path):
        module = __import__(path)
        
        components = path.split(".")
        
        for component in components[1:]:
            module = getattr(module, component)
        
        return module

    @staticmethod
    def qualify_controller_name(name):
        return ("Unrealistic_Engine.controllers." + name)

    @staticmethod
    def quit():
        pygame.event.post (pygame.event.Event(pygame.QUIT))
