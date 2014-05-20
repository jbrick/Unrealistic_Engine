import model
import view
import controller
import pygame
from database import Database
from game_controller import GameController
from game_view import GameView
from position import Position


pygame.init()

size = width, height = 640, 640

screen = pygame.display.set_mode(size)

# Default game model is loaded from a sqlite database.
gameModel = Database().load_application()
gameView = GameView()
gameController = GameController(gameModel, gameView)

gameView.add_model(gameModel.character, GameView.render_character, Position(50, 50))
# Main game loop passes all events to controller and continuaslly renders view.
while True:
    for event in pygame.event.get():
        gameController.handle_game_event(event)
    gameController.check_keys()
    gameView.render(screen)