import pygame

from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.controllers.game_controller import GameController
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine import event_types

pygame.init()

size = width, height = 640, 640

screen = pygame.display.set_mode(size)

# Default game model is loaded from a sqlite database.
model = Database().load_application()
view = GameView()
controller = GameController(model, view)

#Add Map model
view.add_model(model.game_map, GameView.render_map,
               Position(0, 0), 1)
#Add Character model
view.add_model(model.character, GameView.render_character,
               Position(0, 0), 2)


# Main game loop passes all events to controller and continually renders view.
# Draw the screen every 34 ms or 30 fps.
pygame.time.set_timer(event_types.RENDER_SCREEN, 34)
while True:
    for event in pygame.event.get():
        if event.type == event_types.RENDER_SCREEN:
            controller.check_keys()
            view.render(screen)
        # Allow for swapping of MVC Components.
        if event.type == event_types.UPDATE_GAME_STATE:
            controller = event.Controller
            view = event.View
        else:
            controller.handle_game_event(event)
