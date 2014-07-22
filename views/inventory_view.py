import pygame
import os

from Unrealistic_Engine.views.inventory_view_interface import InventoryViewInterface
from Unrealistic_Engine.models.map import Map


class InventoryView(InventoryViewInterface):

    FONT_SIZE = 14
    PADDING = 10

    # Height of each menu item
    LINE_HEIGHT = 25

    # Leaving space for breadcrumbs
    OFFSET = 50
    LARGE_OFFSET = Map.MAP_SIZE - Map.MAP_SIZE/4

    @staticmethod
    def render_background(model, screen, position, *args, **kwargs):
        background = pygame.Surface((Map.MAP_SIZE, Map.MAP_SIZE))
        background.fill((5, 4, 71, 100))
        screen.blit(background, (0, 0))

    @staticmethod
    def render_inventory_menu(inventory_menu, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)
        title_font = pygame.font.SysFont("monospace", 16)

        # Render titles for all of the displays
        title = pygame.font.SysFont("monospace", 20).render("Inventory", 1, (255, 255, 0))
        screen.blit(title, (Map.MAP_SIZE/2 - 60, 10))

        name_title = title_font.render("Name", 1, (255, 255, 0))
        screen.blit(name_title, (2*InventoryView.PADDING, 45))

        quantity_title = title_font.render("Qty", 1, (255, 255, 0))
        screen.blit(quantity_title, (2*InventoryView.PADDING + 250, 45))

        slot_title = title_font.render("Slot", 1, (255, 255, 0))
        screen.blit(slot_title, (2*InventoryView.PADDING + 300, 45))

        equipped_title = title_font.render("Equipped", 1, (255, 255, 0))
        screen.blit(equipped_title, (2*InventoryView.PADDING + 425, 45))

        stats_title = title_font.render("Character Stats", 1, (255, 255, 0))
        screen.blit(stats_title, (InventoryView.LARGE_OFFSET, InventoryView.LARGE_OFFSET))

        description_title = title_font.render("Item Description", 1, (255, 255, 0))
        screen.blit(description_title, (2*InventoryView.PADDING, InventoryView.LARGE_OFFSET))

        # Render menu items
        for count in range(0, len(inventory_menu.nodes)):
            label = font.render(inventory_menu.nodes[count].label, 1, (255, 255, 255))
            screen.blit(label, (2*InventoryView.PADDING,
                        count*InventoryView.LINE_HEIGHT + 75))

            if count == inventory_menu.get_active_node_index():
                screen.blit(inventory_menu.active_icon, (InventoryView.PADDING,
                                                      count*InventoryView.LINE_HEIGHT +
                                                      75 + InventoryView.PADDING))

    @staticmethod
    def render_description(description, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)

        description_label = font.render(description.description, 1, (255, 255, 255))
        screen.blit(description_label, (2*InventoryView.PADDING,
                                        InventoryView.LARGE_OFFSET + 30))


    @staticmethod
    def render_character_data(character, screen, position, *args, **kwargs):
        font = pygame.font.SysFont("monospace", InventoryView.FONT_SIZE)

        # Render inventory list data
        count = 0
        for item in character.inventory.item_list:
            quantity_label = font.render("x " + str(character.inventory.item_list[item]), 1,
                                         (255, 255, 255))
            screen.blit(quantity_label, (2*InventoryView.PADDING + 250,
                        count*InventoryView.LINE_HEIGHT + 75))

            slot_label = font.render(item.slot, 1, (255, 255, 255))
            screen.blit(slot_label, (2*InventoryView.PADDING + 300,
                        count*InventoryView.LINE_HEIGHT + 75))

            if item.slot in character.loadout:
                if character.loadout[item.slot] == item:
                    equipped_image = pygame.image.load(os.path.join('Images', 'check-mark.png'))
                    equipped_image_scaled = pygame.transform.scale(equipped_image, (16, 16))
                    screen.blit(equipped_image_scaled, (2*InventoryView.PADDING + 425,
                                count*InventoryView.LINE_HEIGHT + 75))
            count += 1

        # Render character stats
        health_label = font.render("HP : %d/%d " % (character.health, character.total_health), 1,
                                   (255, 255, 255))
        screen.blit(health_label, (InventoryView.LARGE_OFFSET, InventoryView.LARGE_OFFSET + 24))

        attack_label = font.render("ATK : %d" % character.attack, 1, (255, 255, 255))
        screen.blit(attack_label, (InventoryView.LARGE_OFFSET,
                    InventoryView.LARGE_OFFSET + 24 + InventoryView.LINE_HEIGHT))

        defense_label = font.render("DEF : %d" % character.defense, 1, (255, 255, 255))
        screen.blit(defense_label, (InventoryView.LARGE_OFFSET,
                    InventoryView.LARGE_OFFSET + 24 + 2*InventoryView.LINE_HEIGHT))




