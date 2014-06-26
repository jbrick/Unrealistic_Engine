import pygame


def dictify(list_to_change):
    dictionary = {}
    for item in list_to_change:
        dictionary[item] = item

    return dictionary


def fetch(path):
    module = __import__(path)

    components = path.split(".")

    for component in components[1:]:
        module = getattr(module, component)

    return module


def qualify_model_name(name):
    return "Unrealistic_Engine.models." + name


def qualify_view_name(name):
    return "Unrealistic_Engine.views." + name


def qualify_controller_name(name):
    return "Unrealistic_Engine.controllers." + name

def quit():
    pygame.event.post (pygame.event.Event(pygame.QUIT))
