import pygame
import sys

from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.controllers.title_screen_controller import \
    TitleScreenController
from Unrealistic_Engine.views.title_screen_view import TitleScreenView
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.map import Map


pygame.init()

pygame.display.set_caption('Unrealistic Engine')

size = Map.MAP_SIZE, Map.MAP_SIZE

screen = pygame.display.set_mode(size)

# Default game model is loaded from a sqlite database.
model = Database().load_application()
view = TitleScreenView()
controller = TitleScreenController(model, view)

# Main game loop passes all events to controller and continually renders view.
# Draw the screen every 34 ms or 30 fps.
pygame.time.set_timer(event_types.RENDER_SCREEN, 34)

pygame.key.set_repeat(75, 75)
while True:
    for event in pygame.event.get():
        if event.type is event_types.RENDER_SCREEN:
            view.render(screen)
        if event.type is pygame.KEYDOWN:
            controller.handle_key_press(event.key)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Allow for swapping of MVC Components.
        if event.type == event_types.UPDATE_GAME_STATE:
            controller = event.Controller
            view = event.View
        else:
            controller.handle_game_event(event)
