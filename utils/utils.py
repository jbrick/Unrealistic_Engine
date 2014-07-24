import pygame
from pygame import Rect

from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine import event_types


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


# Attaches LeafNodes representing all saved games to the passed in menu object
def add_saved_game_nodes(parent, action, action_args):
    game_ids = Database().get_saved_games()
    node_ids = []
    for id_on in game_ids:
        new_node = LeafNode("Game "+ str(id_on), action, id_on, action_args)
        node_ids.append(new_node.id)
        parent.nodes.append(new_node)

    return node_ids


def return_to_game(model):
    base = fetch(qualify_controller_name("game_controller"))

    imports = base.GameController.get_imports()

    view_module = fetch(imports[base.GameController.VIEWS]["game_view"])
    view = view_module.GameView()
    controller = base.GameController(model, view)

    Menu.breadcrumbs = []

    pygame.event.post(pygame.event.Event(
        event_types.UPDATE_GAME_STATE, {"Controller": controller, "View": view}))


def qualify_model_name(name):
    return "Unrealistic_Engine.models." + name


def qualify_view_name(name):
    return "Unrealistic_Engine.views." + name


def qualify_controller_name(name):
    return "Unrealistic_Engine.controllers." + name


def quit():
    pygame.event.post (pygame.event.Event(pygame.QUIT))

# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text

