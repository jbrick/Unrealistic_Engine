from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.views.map_view import MapView


# Default view for rendering models
class GameView(MapView):

    # offset in pixels - centres character in tile
    CHARACTER_OFFSET = 0
    
    # For dialogs and incidental text
    FONT_SIZE = 12
    DIALOG_PADDING = 10

    @staticmethod
    def render_character(character, screen, position, *args, **kwargs):
        screen.blit(character.image,
                    position.convert_to_pixels(GameView.CHARACTER_OFFSET))

    @staticmethod
    def render_dialog(dialog, screen, position, *args, **kwargs):
        if dialog.timed:
            if dialog.frame_count > dialog.time_limit:
                pygame.event.post(
                    pygame.event.Event(
                        event_types.KILL_DIALOG,
                        {"Dialog": dialog}))
                return
            else:
                dialog.increment()
        
        # Render the dialog
        font = pygame.font.SysFont("monospace", GameView.FONT_SIZE)
        text = dialog.content
        
        dialog_size = font.size(text)
        dialog_background = pygame.Surface ((dialog_size[0], dialog_size[1]), pygame.SRCALPHA)
        dialog_background.fill((5, 4, 71, 255))
        
        render_position = position.convert_to_pixels(
            -1*(dialog_size[0]/2 + DIALOG_PADDING),
            -1*(dialog_size[1]/2 + DIALOG_PADDING))
        
        screen.blit(dialog_background, render_position)

    @staticmethod
    def render_map(game_map, screen, *args, **kwargs):
        for x in range(0, game_map.grid_size):
            for y in range(0, game_map.grid_size):
                position = Position(x, y)
                if game_map.tiles[x][y] != 0:
                    screen.blit(game_map.tiles[x][y].image,
                                position.convert_to_pixels(0))
