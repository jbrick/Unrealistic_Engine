import pygame

from Unrealistic_Engine.views.view import View
from Unrealistic_Engine import event_types

class DialogView(View):

    # For dialogs and incidental text
    FONT_SIZE = 12
    DIALOG_PADDING = 10

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
        font = pygame.font.SysFont("monospace", DialogView.FONT_SIZE)
        text = dialog.content

        dialog_size = font.size(text)
        dialog_background = pygame.Surface ((
            dialog_size[0] + 2*DialogView.DIALOG_PADDING,
            dialog_size[1] + 2*DialogView.DIALOG_PADDING), pygame.SRCALPHA)
        dialog_background.fill((5, 4, 71, 255))

        render_position = position.convert_with_offset(
            -1*(dialog_size[0]/2 + DialogView.DIALOG_PADDING),
            -1*(dialog_size[1]/2 + DialogView.DIALOG_PADDING))

        screen.blit(dialog_background, render_position)

        label = font.render(dialog.content, 1, (255, 255, 255))

        screen.blit(label, (
                render_position[0] + DialogView.DIALOG_PADDING,
                render_position[1] + DialogView.DIALOG_PADDING))