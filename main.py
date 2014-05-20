import pygame
from Unrealistic_Engine.models.database import Database
from Unrealistic_Engine.controllers.game_controller import GameController
from Unrealistic_Engine.views.game_view import GameView
from Unrealistic_Engine.utils.position import Position

RENDER_SCREEN = pygame.USEREVENT + 1

pygame.init()

size = width, height = 640, 640

screen = pygame.display.set_mode(size)

# Default game model is loaded from a sqlite database.
gameModel = Database().load_application()
gameView = GameView()
gameController = GameController(gameModel, gameView)

gameView.add_model(gameModel.character, GameView.render_character, Position(50, 50))
# Main game loop passes all events to controller and continuaslly renders view.

# Draw the screen every 34 ms or 30 fps.
pygame.time.set_timer(RENDER_SCREEN, 34)
while True:
    for event in pygame.event.get():
        if event.type == RENDER_SCREEN:
            gameController.check_keys()
            gameView.render(screen)
        else:
            gameController.handle_game_event(event)
