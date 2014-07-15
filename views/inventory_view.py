import pygame

from Unrealistic_Engine.views.inventory_view_interface import InventoryViewInterface
from Unrealistic_Engine.models.map import Map


class InventoryView(InventoryViewInterface):

    FONT_SIZE = 16
    PADDING = 10

    # Height of each menu item
    LINE_HEIGHT = 25

    # Leaving space for breadcrumbs
    OFFSET = 50

    @staticmethod
    def render_inventory(inventory, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)

        background = pygame.Surface((Map.MAP_SIZE, Map.MAP_SIZE))
        background.fill((5, 4, 71, 100))
        screen.blit(background, (0, 0))

        count = 0
        for item in inventory.item_list:
            name_label = font.render(item.name, 1, (255, 255, 255))
            screen.blit(name_label, (2*InventoryView.PADDING,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))

            quantity_label = font.render(str(inventory.item_list[item]), 1, (255, 255, 255))
            screen.blit(quantity_label, (2*InventoryView.PADDING + Map.MAP_SIZE/2,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))
            count += 1


