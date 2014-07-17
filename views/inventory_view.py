import pygame

from Unrealistic_Engine.views.inventory_view_interface import InventoryViewInterface
from Unrealistic_Engine.models.map import Map


class InventoryView(InventoryViewInterface):

    FONT_SIZE = 14
    PADDING = 10

    # Height of each menu item
    LINE_HEIGHT = 25

    # Leaving space for breadcrumbs
    OFFSET = 50

    @staticmethod
    def render_background(model, screen, position, *args, **kwargs):
        background = pygame.Surface((Map.MAP_SIZE, Map.MAP_SIZE))
        background.fill((5, 4, 71, 100))
        screen.blit(background, (0, 0))

    @staticmethod
    def render_inventory_menu(inventory_menu, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)


        # Render menu items
        for count in range(0, len(inventory_menu.nodes)):
            label = font.render(inventory_menu.nodes[count].label, 1, (255, 255, 255))
            screen.blit(label, (2*InventoryView.PADDING,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))

            if count == inventory_menu.get_active_node_index():
                screen.blit(inventory_menu.active_icon, (InventoryView.PADDING,
                                                      count*InventoryView.LINE_HEIGHT +
                                                      InventoryView.OFFSET + InventoryView.PADDING))

    @staticmethod
    def render_description(description, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)


    @staticmethod
    def render_character_data(character, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)


        # Render inventory list data
        count = 0
        for item in character.inventory.item_list:
            quantity_label = font.render(str(character.inventory.item_list[item]), 1, (255, 255, 255))
            screen.blit(quantity_label, (2*InventoryView.PADDING + 200,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))

            type_label = font.render((item).__class__.__name__, 1, (255, 255, 255))
            screen.blit(type_label, (2*InventoryView.PADDING + 250,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))

            slot_label = font.render(item.slot, 1, (255, 255, 255))
            screen.blit(slot_label, (2*InventoryView.PADDING + 400,
                        count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))

            if item.slot in character.loadout:
                if character.loadout[item.slot] == item:
                    equipped_label = font.render(str(1), 1, (255, 255, 255))
                    screen.blit(equipped_label, (2*InventoryView.PADDING + 350,
                                count*InventoryView.LINE_HEIGHT + InventoryView.OFFSET))
            count += 1

        # Render character stats


